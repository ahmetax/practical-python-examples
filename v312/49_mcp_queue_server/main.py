# Author: Ahmet Aksoy & Claude
# Date: 26.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.10+ and mcp>=2 (pip install "mcp>=2,<3")

"""
Read-Only MCP Server for a WordPress Publishing Queue
Exposes a WordPress site's scheduled posts to an MCP client (Claude Code, Claude
Desktop, ...) as three read-only tools. There is deliberately no tool that
creates, edits or publishes posts.

    python main.py            # serve over stdio (WP_URL, WP_USER, WP_APP_PASSWORD)
    python main.py --demo     # serve over stdio with built-in sample data
    python main.py --check    # start the demo server as a client and call every tool

mcp 2.x renamed FastMCP to MCPServer: `from mcp.server.fastmcp import FastMCP`
raises ModuleNotFoundError on mcp>=2. Never print() to stdout in a stdio server;
write diagnostics to sys.stderr.
"""
import base64
import http.client
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

PUBLISH_DAYS = (0, 3)  # Monday, Thursday
PUBLISH_HOUR = 10
LATE_MARGIN = timedelta(minutes=30)  # WP-Cron publishes only when the site gets a request
DEMO = "--demo" in sys.argv

mcp = MCPServer("wp-queue")
READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=True)


def demo_posts(status: str) -> list[dict]:
    today = datetime.now().replace(hour=PUBLISH_HOUR, minute=0, second=0, microsecond=0)
    base, days = (200, (3, 7)) if status == "future" else (100, (-1, -4, -8))
    return [{"id": base + i, "date": (today + timedelta(days=d)).isoformat(),
             "title": {"rendered": f"Sample {status} post {i + 1}"},
             "link": f"https://example.com/?p={base + i}"} for i, d in enumerate(days)]


def wp_get(path: str) -> list[dict]:
    # An undefined ${VAR} in an MCP client config may arrive as the literal text "${VAR}".
    missing = [k for k in ("WP_URL", "WP_USER", "WP_APP_PASSWORD")
               if not os.environ.get(k) or os.environ[k].startswith("${")]
    if missing:
        raise ToolError(f"Missing or unexpanded environment variable(s): {', '.join(missing)}. "
                        "The MCP client must pass them when it starts the server.")
    auth = base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    req = urllib.request.Request(os.environ["WP_URL"].rstrip("/") + "/wp-json/wp/v2" + path,
                                 headers={"Authorization": "Basic " + auth, "User-Agent": "wp-queue-mcp/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise ToolError(f"WordPress HTTP {exc.code}: {exc.read().decode()[:200]}") from exc
    except (OSError, http.client.HTTPException, ValueError) as exc:
        raise ToolError(f"Cannot reach WordPress: {exc}") from exc
    if not isinstance(data, list):
        raise ToolError(f"Unexpected response: {str(data)[:200]}")
    return data


def posts(status: str, count: int = 100) -> list[dict]:
    if DEMO:
        return demo_posts(status)[:count]
    order = "asc" if status == "future" else "desc"
    return wp_get(f"/posts?status={status}&per_page={count}&orderby=date&order={order}"
                  "&_fields=id,date,title,link")


def summary(post: dict) -> dict:
    when = datetime.fromisoformat(post["date"])
    return {"id": post["id"], "date": post["date"], "weekday": when.strftime("%A"),
            "title": post["title"]["rendered"], "link": post["link"]}


@mcp.tool(annotations=READ_ONLY)
def publish_queue() -> list[dict]:
    """List the site's scheduled (not yet published) posts, oldest first.

    Each item: id, date (site time, ISO), weekday, title, link. Links of scheduled
    posts return 404 to visitors until the publish date.
    """
    return [summary(p) for p in posts("future")]


@mcp.tool(annotations=READ_ONLY)
def queue_status(weeks: int = 4) -> dict:
    """Check the queue against its rule and list upcoming empty publish slots.

    Rule: at least one scheduled post at all times; publish slots are Monday and
    Thursday 10:00. Status is OK, WARNING or CRITICAL.
    weeks: how many weeks of publish slots to scan (1-12).
    """
    weeks = max(1, min(weeks, 12))
    queue = posts("future")
    now = datetime.now().replace(microsecond=0)
    dates = {datetime.fromisoformat(p["date"]) for p in queue}
    empty = []
    slot = now.replace(hour=PUBLISH_HOUR, minute=0, second=0)
    while slot <= now + timedelta(weeks=weeks):
        if slot > now and slot.weekday() in PUBLISH_DAYS and slot not in dates:
            empty.append(slot.strftime("%Y-%m-%d %A %H:%M"))
        slot += timedelta(days=1)
    if not queue:
        status, message = "CRITICAL", "No scheduled posts."
    elif any(d < now - LATE_MARGIN for d in dates):
        status, message = "CRITICAL", "A scheduled post is past its time but not published (check WP-Cron)."
    elif len(queue) == 1 or (empty and empty[0] < min(dates).strftime("%Y-%m-%d")):
        status, message = "WARNING", f"{len(queue)} scheduled post(s); the next slot is empty or only one post is left."
    else:
        status, message = "OK", f"{len(queue)} scheduled posts, the last on {max(dates):%Y-%m-%d %H:%M}."
    return {"status": status, "message": message, "scheduled": len(queue),
            "empty_slots": empty, "checked_at": now.isoformat(), "demo": DEMO}


@mcp.tool(annotations=READ_ONLY)
def recent_posts(count: int = 5) -> list[dict]:
    """List the most recently published posts, newest first (count: 1-20)."""
    return [summary(p) for p in posts("publish", max(1, min(count, 20)))]


def check() -> None:
    """Start this file with --demo as a stdio server and call every tool once."""
    import anyio
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def run() -> None:
        params = StdioServerParameters(command=sys.executable, args=[__file__, "--demo"])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                for tool in (await session.list_tools()).tools:
                    print(f"tool {tool.name:<14} read_only={tool.annotations.read_only_hint}")
                for name, args in (("queue_status", {"weeks": 2}), ("publish_queue", {}), ("recent_posts", {"count": 2})):
                    result = await session.call_tool(name, args)
                    body = result.structured_content or json.loads(result.content[0].text)
                    print(f"\n{name}({args}) ->\n{json.dumps(body, indent=1)}")

    anyio.run(run)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        mcp.run(transport="stdio")
