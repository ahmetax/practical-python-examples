# Project 52: An MCP Server With One Guarded Write Tool (WordPress Drafts)

A follow-up to [project 49](../49_mcp_queue_server/), a read-only MCP server. This one adds a single write tool, `upload_draft`, and puts several guards in front of it. The most important one: **the confirmation comes from the user, not from the model.** The server asks the user through the MCP client (elicitation). A confirmation code handed to the model is not a human confirmation, because the model can pass it on by itself.

| Guard | What it does |
|-------|--------------|
| Dry run by default | `dry_run=True` writes nothing and returns the summary and the problems found |
| Human confirmation | `dry_run=False`: the server asks the user via the client; no answer, `decline` or `cancel` means nothing is written |
| Fixed status | Posts are always created with `status=draft`; scheduling and publishing are not parameters |
| Narrow scope | Only `POSTS_DIR/<folder>/post.json`; no update or delete; a used slug, a taken slot (scheduled **or draft**) or a date that is not Monday/Thursday 10:00 is refused; missing categories/tags are not created |
| Limit and trail | At most 2 writes per server process; every attempt goes to `draft_log.jsonl` with the negotiated protocol version |

There is also one read-only tool, `publish_queue`.

## Project Structure
```text
52_mcp_draft_guard/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer and `mcp>=2,<3`. Tested with Python 3.12.3, `mcp` 2.3.0 and Claude Code 2.1.319 on Ubuntu 24.04.
- For a real site: a WordPress Application Password in `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`. `--demo` and `--check` need nothing.

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp>=2,<3"
```

## Running
```bash
.venv/bin/python main.py --check   # start the demo server as a client and run the confirmation scenarios
.venv/bin/python main.py --demo    # stdio server with an in-memory fake site
.venv/bin/python main.py           # stdio server for a real site
```

A post folder (default `POSTS_DIR` is `./posts`) looks like this. The text is sent as plain paragraphs:
```json
{"title": "My post", "slug": "my-post", "date": "2026-11-23T10:00:00", "markdown": "post.md",
 "excerpt": "Short summary.", "categories": ["python"], "tags": ["mcp"]}
```

## Example Output (`--check`, Python 3.12.3, mcp 2.3.0)
```text

== 1. Dry run (default)
  upload_draft({'folder': 'sample-post'}) -> {"written": false, "problems": []}

== 2. Client cannot ask the user
  upload_draft({'folder': 'sample-post', 'dry_run': False}) -> PROTOCOL ERROR: Client did not declare the form elicitation capability required by resolver '__main__:ask_user'

== 3. User declines
    [asked the user] Upload a DRAFT to WordPress? |  Title: Sample: sample-post |  Slug: sample-post |  Planned: 2026-11-16 10:00 Monday |  6 words, status: draft
  upload_draft({'folder': 'sample-post', 'dry_run': False}) -> {"written": false, "problems": ["The user did not confirm (decline). Nothing was written."]}

== 4. User confirms; then the same folder again, then another post for the same slot
    [asked the user] Upload a DRAFT to WordPress? |  Title: Sample: sample-post |  Slug: sample-post |  Planned: 2026-11-16 10:00 Monday |  6 words, status: draft
  upload_draft({'folder': 'sample-post', 'dry_run': False}) -> {"written": true, "post_id": 500, "status": "draft"}
  upload_draft({'folder': 'sample-post', 'dry_run': False}) -> {"written": false, "problems": ["2026-11-16 10:00 already has a post: ID 500 (draft).", "Slug 'sample-post' is already used."]}
  upload_draft({'folder': 'same-slot', 'dry_run': False}) -> {"written": false, "problems": ["2026-11-16 10:00 already has a post: ID 500 (draft)."]}

== 5. Outside POSTS_DIR, and a Sunday date
  upload_draft({'folder': '../..'}) -> ERROR: Error executing tool upload_draft: Only a folder directly under POSTS_DIR can be uploaded (got '../..').
  upload_draft({'folder': 'sunday-post', 'dry_run': False}) -> {"written": false, "problems": ["2026-11-15 10:00 (Sunday) is not a publish slot."]}
```
Dates depend on the day you run it. The demo site lives in memory, so each session starts empty.

## Notes From the Experiments
- **`ctx.elicit()` failed in Claude Code.** The `mcp` Python client connected with protocol `2025-11-25`, where the server sends `elicitation/create` in the middle of a tool call. Claude Code 2.1.319 connected with `2026-07-28`, where the server returns an `InputRequiredResult` and the client calls the tool again with the answer. `ctx.elicit()` raised `NoBackChannelError`. A resolver that returns `Elicit(...)` (`Annotated[..., Resolve(fn)]`) works on both.
- **In `claude -p` the question cannot be shown,** so Claude Code answered `cancel` and nothing was written, also when the prompt said "no need to ask me".
- **A two-step confirmation code was not enough.** With "no need to ask me" in the prompt, the model passed the code to the second tool itself.
- **Permission modes are a separate layer.** In Claude Code's `auto` mode the write tool was called without a permission prompt despite `read_only_hint=False`; only the server's own confirmation stopped the write.
- **An Application Password carries all the rights of its user.** Running the server as a WordPress user with the Contributor role adds a guard on the WordPress side (not done here).
- A Claude Code `Elicitation` hook can answer the question without showing it. That is user configuration, not model behavior, but keep it in mind.

## References
- Blog post (Turkish): https://gurmezin.com/2026/11/23/mcp-sunucusuna-yazma-araci-onayi-kullaniciya-sordurduk/
- MCP specification 2026-07-28, Elicitation: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- Claude Code MCP documentation: https://code.claude.com/docs/en/mcp
