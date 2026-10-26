# Project 49: Read-Only MCP Server for a WordPress Publishing Queue

An MCP (Model Context Protocol) server that exposes a WordPress site's scheduled posts to an MCP client such as Claude Code as three **read-only** tools. There is deliberately no tool that creates, edits or publishes posts: a tool the model does not have cannot be misused.

| Tool | What it returns |
|------|-----------------|
| `publish_queue` | Scheduled (future) posts, oldest first |
| `queue_status(weeks=4)` | OK / WARNING / CRITICAL against the rule "always at least one scheduled post" and the empty Monday/Thursday 10:00 slots |
| `recent_posts(count=5)` | The latest published posts |

## Project Structure
```text
49_mcp_queue_server/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer (required by `mcp` 2.x) and `mcp>=2,<3`. Tested with Python 3.12.3, `mcp` 2.3.0 and Claude Code 2.1.310 on Ubuntu 24.04.
- For a real site: a WordPress Application Password in `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`. `--demo` and `--check` need nothing.

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp>=2,<3"
```

## Running
```bash
.venv/bin/python main.py --check   # start the demo server as a client, call every tool
.venv/bin/python main.py --demo    # stdio server with sample data
.venv/bin/python main.py           # stdio server for a real site
```

To use it in Claude Code, put a `.mcp.json` in your project. Write the credentials as `${...}` references, not as values:
```json
{
  "mcpServers": {
    "wp-queue": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/main.py"],
      "env": {"WP_URL": "${WP_URL}", "WP_USER": "${WP_USER}", "WP_APP_PASSWORD": "${WP_APP_PASSWORD}"}
    }
  }
}
```

## Sample Output (`--check`, Python 3.12.3, mcp 2.3.0)
```text
tool publish_queue  read_only=True
tool queue_status   read_only=True
tool recent_posts   read_only=True

queue_status({'weeks': 2}) ->
{
 "status": "OK",
 "message": "2 scheduled posts, the last on 2026-11-02 10:00.",
 "scheduled": 2,
 "empty_slots": [
  "2026-11-05 Thursday 10:00",
  "2026-11-09 Monday 10:00"
 ],
 "checked_at": "2026-10-26T12:20:35",
 "demo": true
}

publish_queue({}) ->
{
 "result": [
  {
   "id": 200,
   "date": "2026-10-29T10:00:00",
   "weekday": "Thursday",
   "title": "Sample future post 1",
   "link": "https://example.com/?p=200"
  },
  {
   "id": 201,
   "date": "2026-11-02T10:00:00",
   "weekday": "Monday",
   "title": "Sample future post 2",
   "link": "https://example.com/?p=201"
  }
 ]
}

recent_posts({'count': 2}) ->
{
 "result": [
  {
   "id": 100,
   "date": "2026-10-25T10:00:00",
   "weekday": "Sunday",
   "title": "Sample publish post 1",
   "link": "https://example.com/?p=100"
  },
  {
   "id": 101,
   "date": "2026-10-22T10:00:00",
   "weekday": "Thursday",
   "title": "Sample publish post 2",
   "link": "https://example.com/?p=101"
  }
 ]
}
```
Dates are relative to the day you run it.

## Notes From Testing
- **mcp 2.x renamed FastMCP to MCPServer** (2.0.0, 28 July 2026). `from mcp.server.fastmcp import FastMCP`, found in most tutorials, raises `ModuleNotFoundError`. Pin the major version.
- **Environment variables depend on the client.** The `mcp` Python client passes only `HOME, LOGNAME, PATH, SHELL, TERM, USER` by default; Claude Code passes its whole environment. An undefined `${WP_URL}` in a Claude Code config arrives as the literal text `${WP_URL}`, so the server treats values starting with `${` as missing.
- **stdout:** with mcp 2.x the server diverts fd 1 to stderr while serving, and neither the Python client nor Claude Code broke on stray lines in our tests (1.30.0 and 2.3.0). Still, write diagnostics to `sys.stderr`: where a `print()` ends up depends on buffering, version and client.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/11/09/python-ile-mcp-sunucusu-yayin-kuyrugu-claude-salt-okunur-arac/
- MCP Python SDK v2 migration guide: https://py.sdk.modelcontextprotocol.io/v2/migration/
- Claude Code MCP documentation: https://code.claude.com/docs/en/mcp
