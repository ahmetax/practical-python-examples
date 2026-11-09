# Author: Ahmet Aksoy & Claude
# Date: 09.11.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.10+ and mcp>=2 (pip install "mcp>=2,<3")

"""
MCP Server With One Guarded Write Tool: Upload a WordPress Draft
Adds a single write tool, upload_draft, next to a read-only queue tool. The guards,
outermost first:

  1. Dry run by default: dry_run=True sends nothing and returns what would be sent.
  2. Human confirmation through MCP elicitation (a Resolve/Elicit resolver, which works
     on both protocol eras): the server asks the *user* via the client. If the client
     cannot ask (no elicitation support), nothing is written.
     A confirmation code handed to the model is NOT a human confirmation: the model
     can pass it on by itself.
  3. Fixed status: posts are always created with status=draft. Scheduling and
     publishing are not parameters of this server.
  4. Narrow scope: only <POSTS_DIR>/<folder>/post.json can be uploaded; existing posts
     are never updated or deleted; a used slug or a taken/invalid date is refused;
     missing categories/tags are not created.
  5. Limit and trail: at most 2 writes per server process; every attempt is logged.

    python main.py            # stdio server for a real site (WP_URL, WP_USER, WP_APP_PASSWORD)
    python main.py --demo     # stdio server with an in-memory fake site and sample posts
    python main.py --check    # start the demo server as a client and run the scenarios
"""
import base64
import html
import http.client
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field

from mcp.server.mcpserver import AcceptedElicitation, Context, Elicit, ElicitationResult, MCPServer, Resolve
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

PUBLISH_DAYS = (0, 3)  # Monday, Thursday
PUBLISH_HOUR = 10
MAX_WRITES = 2
DEMO = "--demo" in sys.argv
POSTS_DIR = Path(os.environ.get("POSTS_DIR", Path(__file__).with_name("posts"))).resolve()
LOG = Path(os.environ.get("DRAFT_LOG", Path(__file__).with_name("draft_log.jsonl")))

mcp = MCPServer("wp-drafts")
READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=True)
WRITE = ToolAnnotations(read_only_hint=False, destructive_hint=False, idempotent_hint=False, open_world_hint=True)
_writes = 0
_demo_site = {"posts": [], "categories": [{"id": 1, "name": "python"}], "tags": [{"id": 10, "name": "mcp"}]}


class Confirm(BaseModel):
    confirm: bool = Field(description="Upload this draft to WordPress?")


def log(**entry) -> None:
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"time": datetime.now().isoformat(timespec="seconds"), **entry}) + "\n")


def wp(path: str, body: dict | None = None):
    if DEMO:
        return demo_wp(path, body)
    missing = [k for k in ("WP_URL", "WP_USER", "WP_APP_PASSWORD")
               if not os.environ.get(k) or os.environ[k].startswith("${")]
    if missing:
        raise ToolError(f"Missing or unexpanded environment variable(s): {', '.join(missing)}.")
    auth = base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    headers = {"Authorization": "Basic " + auth, "User-Agent": "wp-drafts-mcp/1.0"}
    data = None
    if body is not None:
        data, headers["Content-Type"] = json.dumps(body).encode(), "application/json"
    req = urllib.request.Request(os.environ["WP_URL"].rstrip("/") + "/wp-json/wp/v2" + path, data=data,
                                 headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise ToolError(f"WordPress HTTP {exc.code}: {exc.read().decode()[:200]}") from exc
    except (OSError, http.client.HTTPException, ValueError) as exc:
        raise ToolError(f"Cannot reach WordPress: {exc}") from exc


def demo_wp(path: str, body: dict | None):
    if body is not None:
        post = {"id": 500 + len(_demo_site["posts"]), **body}
        _demo_site["posts"].append(post)
        return post
    url = urllib.parse.urlparse(path)
    q = dict(urllib.parse.parse_qsl(url.query))
    if url.path == "/posts":
        statuses = q.get("status", "publish").split(",")
        return [p for p in _demo_site["posts"] if p["status"] in statuses and q.get("slug", p["slug"]) == p["slug"]]
    return [t for t in _demo_site[url.path[1:]] if q.get("search", "").lower() in t["name"].lower()]


def find_terms(kind: str, names: list[str]) -> tuple[list[int], list[str]]:
    found, missing = [], []
    for name in names:
        ids = [t["id"] for t in wp(f"/{kind}?search={urllib.parse.quote(name)}&per_page=100&_fields=id,name")
               if t["name"].lower() == name.lower()]
        (found.append(ids[0]) if ids else missing.append(name))
    return found, missing


def resolve_folder(folder: str) -> Path:
    path = (POSTS_DIR / folder).resolve()
    if path.parent != POSTS_DIR:
        raise ToolError(f"Only a folder directly under POSTS_DIR can be uploaded (got {folder!r}).")
    if not (path / "post.json").is_file():
        raise ToolError(f"{path.name} has no post.json.")
    return path


def prepare(path: Path) -> tuple[dict, dict, list[str]]:
    meta = json.loads((path / "post.json").read_text(encoding="utf-8"))
    when = datetime.fromisoformat(meta["date"])
    problems = []
    if when.weekday() not in PUBLISH_DAYS or (when.hour, when.minute) != (PUBLISH_HOUR, 0):
        problems.append(f"{when:%Y-%m-%d %H:%M} ({when:%A}) is not a publish slot.")
    if when <= datetime.now():
        problems.append("The date is in the past.")
    # Checking scheduled posts is not enough: an earlier draft may already hold the slot.
    for p in wp("/posts?status=future,draft,pending&per_page=100&_fields=id,date,status"):
        if datetime.fromisoformat(p["date"]) == when:
            problems.append(f"{when:%Y-%m-%d %H:%M} already has a post: ID {p['id']} ({p['status']}).")
    if wp(f"/posts?slug={urllib.parse.quote(meta['slug'])}&status=draft,pending,future,publish&_fields=id"):
        problems.append(f"Slug {meta['slug']!r} is already used.")
    cats, missing_c = find_terms("categories", meta.get("categories", []))
    tags, missing_t = find_terms("tags", meta.get("tags", []))
    text = (path / meta["markdown"]).read_text(encoding="utf-8")
    content = "\n".join(f"<p>{html.escape(p.strip())}</p>" for p in text.split("\n\n") if p.strip())
    body = {"title": meta["title"], "slug": meta["slug"], "content": content, "excerpt": meta.get("excerpt", ""),
            "status": "draft", "date": meta["date"], "categories": cats, "tags": tags}
    summary = {"folder": path.name, "title": meta["title"], "slug": meta["slug"],
               "planned": f"{when:%Y-%m-%d %H:%M %A}", "status": "draft (schedule and publish by hand)",
               "words": len(text.split()), "terms_not_created": missing_c + missing_t}
    return body, summary, problems


@mcp.tool(annotations=READ_ONLY)
def publish_queue() -> list[dict]:
    """List scheduled (future) posts, oldest first: id, date, title."""
    return [{"id": p["id"], "date": p["date"], "title": p["title"] if DEMO else p["title"]["rendered"]}
            for p in wp("/posts?status=future&per_page=100&orderby=date&order=asc&_fields=id,date,title")]


def question(summary: dict) -> str:
    return (f"Upload a DRAFT to WordPress?\n  Title: {summary['title']}\n  Slug: {summary['slug']}\n"
            f"  Planned: {summary['planned']}\n  {summary['words']} words, status: draft")


async def ask_user(folder: str, dry_run: bool = True) -> str | Elicit[Confirm]:
    """Resolver that asks the user before the tool body runs.

    ctx.elicit() only works on the older protocol (<= 2025-11-25), where the server can send
    the client a request in the middle of a tool call. Protocol 2026-07-28 has no such
    back-channel (NoBackChannelError). A resolver that returns Elicit works on both: on the
    new protocol the server returns an "input required" result and the client calls the tool
    again with the user's answer. No question is asked on a dry run or when a check fails.
    """
    if dry_run:
        return "dry_run"
    _, summary, problems = prepare(resolve_folder(folder))
    if problems or _writes >= MAX_WRITES:
        return "not_asked"
    return Elicit(question(summary), Confirm)


@mcp.tool(annotations=WRITE)
async def upload_draft(
    folder: str,
    ctx: Context,
    confirmation: Annotated[ElicitationResult[Confirm], Resolve(ask_user)],
    dry_run: bool = True,
) -> dict:
    """Upload POSTS_DIR/<folder>/post.json to WordPress as a DRAFT.

    dry_run=True (default): nothing is written; returns the summary and any problems.
    dry_run=False: the server asks the user directly for confirmation; the confirmation
    comes from the user, not from the model. Posts are always drafts: this tool cannot
    schedule, publish, update or delete posts, and does not create categories or tags.
    The date must be an empty Monday/Thursday 10:00 slot.
    """
    global _writes
    path = resolve_folder(folder)
    body, summary, problems = prepare(path)
    proto = ctx.protocol_version
    if dry_run or problems:
        log(folder=path.name, dry_run=dry_run, result="blocked" if problems else "dry_run", problems=problems,
            protocol=proto)
        return {"dry_run": dry_run, "written": False, "summary": summary, "problems": problems}
    if _writes >= MAX_WRITES:
        log(folder=path.name, dry_run=False, result="limit", protocol=proto)
        raise ToolError(f"At most {MAX_WRITES} drafts per server process. Restart the server.")
    if not (isinstance(confirmation, AcceptedElicitation) and isinstance(confirmation.data, Confirm)
            and confirmation.data.confirm):
        log(folder=path.name, dry_run=False, result="declined", action=confirmation.action, protocol=proto)
        return {"dry_run": False, "written": False, "summary": summary,
                "problems": [f"The user did not confirm ({confirmation.action}). Nothing was written."]}
    _writes += 1
    post = wp("/posts", body)
    log(folder=path.name, dry_run=False, result="written", post_id=post["id"], status=post["status"], protocol=proto)
    return {"dry_run": False, "written": True, "post_id": post["id"], "status": post["status"], "summary": summary}


def make_sample_posts(root: Path) -> None:
    monday = datetime.now().replace(hour=PUBLISH_HOUR, minute=0, second=0, microsecond=0)
    monday += timedelta(days=(7 - monday.weekday()) or 7)
    for name, when in (("sample-post", monday), ("same-slot", monday), ("sunday-post", monday - timedelta(days=1))):
        (root / name).mkdir()
        (root / name / "post.md").write_text("Hello.\n\nThis is a sample draft.\n", encoding="utf-8")
        (root / name / "post.json").write_text(json.dumps(
            {"title": f"Sample: {name}", "slug": name, "date": when.isoformat(), "markdown": "post.md",
             "excerpt": "Sample.", "categories": ["python", "news"], "tags": ["mcp"]}), encoding="utf-8")


def check() -> None:
    """Start this file with --demo as a stdio server and run the confirmation scenarios.

    Each session starts a new server process, so the in-memory demo site starts empty.
    """
    import anyio
    import mcp.types as types
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import get_default_environment, stdio_client
    from mcp.shared.exceptions import MCPError

    def answering(action: str, confirm: bool = True):
        async def callback(context, params):
            print("    [asked the user] " + params.message.replace("\n", " |"))
            return types.ElicitResult(action=action, content={"confirm": confirm} if action == "accept" else None)
        return callback

    def show(result) -> str:
        if result.is_error:
            return "ERROR: " + result.content[0].text
        body = result.structured_content or json.loads(result.content[0].text)
        return json.dumps({k: body[k] for k in ("written", "post_id", "status", "problems") if k in body})

    async def session(title, calls, root, callback=None):
        print(f"\n== {title}")
        env = {**get_default_environment(), "POSTS_DIR": str(root), "DRAFT_LOG": str(root / "log.jsonl")}
        params = StdioServerParameters(command=sys.executable, args=[__file__, "--demo"], env=env)
        async with stdio_client(params) as (read, write), \
                ClientSession(read, write, elicitation_callback=callback) as s:
            await s.initialize()
            for args in calls:
                try:
                    shown = show(await s.call_tool("upload_draft", args))
                except MCPError as exc:  # protocol-level error, not a tool result
                    shown = f"PROTOCOL ERROR: {exc}"
                print(f"  upload_draft({args}) -> {shown}")

    async def run():
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make_sample_posts(root)
            a = {"folder": "sample-post", "dry_run": False}
            await session("1. Dry run (default)", [{"folder": "sample-post"}], root)
            await session("2. Client cannot ask the user", [a], root)
            await session("3. User declines", [a], root, answering("decline"))
            await session("4. User confirms; then the same folder again, then another post for the same slot",
                          [a, a, {"folder": "same-slot", "dry_run": False}], root, answering("accept"))
            await session("5. Outside POSTS_DIR, and a Sunday date",
                          [{"folder": "../.."}, {"folder": "sunday-post", "dry_run": False}], root, answering("accept"))
            print("\nlog:\n" + (root / "log.jsonl").read_text())

    anyio.run(run)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        mcp.run(transport="stdio")
