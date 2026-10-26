# Proje 49: WordPress Yayın Kuyruğu İçin Salt Okunur MCP Sunucusu

Bir WordPress sitesinin zamanlanmış yazılarını Claude Code gibi bir MCP (Model Context Protocol) istemcisine **yalnızca okuyan** üç araç olarak sunan sunucu. Yazı oluşturan, değiştiren ya da yayınlayan bir araç bilerek yok: modelin elinde olmayan bir araç yanlış kullanılamaz.

| Araç | Döndürdüğü |
|------|------------|
| `publish_queue` | Zamanlanmış (future) yazılar, eskiden yeniye |
| `queue_status(weeks=4)` | "Her zaman en az bir zamanlanmış yazı" kuralına göre OK / WARNING / CRITICAL ve boş Pazartesi/Perşembe 10:00 günleri |
| `recent_posts(count=5)` | Son yayınlanan yazılar |

## Proje Yapısı
```text
49_mcp_queue_server/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.10 veya üstü (`mcp` 2.x bunu istiyor) ve `mcp>=2,<3`. Python 3.12.3, `mcp` 2.3.0 ve Claude Code 2.1.310 ile Ubuntu 24.04'te test edildi.
- Gerçek bir site için `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` değişkenlerinde bir WordPress uygulama şifresi. `--demo` ve `--check` hiçbir şey gerektirmez.

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp>=2,<3"
```

## Çalıştırma
```bash
.venv/bin/python main.py --check   # örnek veriyle sunucuyu istemci olarak başlatır, her aracı çağırır
.venv/bin/python main.py --demo    # örnek veriyle stdio sunucusu
.venv/bin/python main.py           # gerçek site için stdio sunucusu
```

Claude Code'da kullanmak için projenize bir `.mcp.json` koyun. Kimlik bilgilerini değer olarak değil, `${...}` başvurusu olarak yazın:
```json
{
  "mcpServers": {
    "wp-queue": {
      "command": "/yol/.venv/bin/python",
      "args": ["/yol/main.py"],
      "env": {"WP_URL": "${WP_URL}", "WP_USER": "${WP_USER}", "WP_APP_PASSWORD": "${WP_APP_PASSWORD}"}
    }
  }
}
```

## Örnek Çıktı (`--check`, Python 3.12.3, mcp 2.3.0)
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
Tarihler, betiği çalıştırdığınız güne göre değişir.

## Denemelerden Notlar
- **mcp 2.x'te FastMCP'nin adı MCPServer oldu** (2.0.0, 28 Temmuz 2026). Öğreticilerin çoğundaki `from mcp.server.fastmcp import FastMCP` satırı `ModuleNotFoundError` verir. Ana sürümü sabitleyin.
- **Ortam değişkenleri istemciye bağlı.** `mcp` Python istemcisi varsayılan olarak yalnızca `HOME, LOGNAME, PATH, SHELL, TERM, USER` geçirir; Claude Code kendi ortamının tamamını geçirir. Claude Code yapılandırmasındaki tanımsız bir `${WP_URL}`, sunucuya `${WP_URL}` metni olarak ulaşır; bu yüzden sunucu `${` ile başlayan değerleri eksik sayar.
- **stdout:** mcp 2.x sunucusu çalışırken 1 numaralı tanımlayıcıyı stderr'e yönlendiriyor. Denemelerimizde (1.30.0 ve 2.3.0) ne Python istemcisi ne Claude Code kaçak satırlarla bozuldu. Yine de tanılama mesajlarını `sys.stderr`'e yazın: bir `print()` çıktısının nereye gideceği tampona, sürüme ve istemciye bağlı.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/11/09/python-ile-mcp-sunucusu-yayin-kuyrugu-claude-salt-okunur-arac/
- MCP Python SDK v2 geçiş rehberi: https://py.sdk.modelcontextprotocol.io/v2/migration/
- Claude Code MCP belgeleri: https://code.claude.com/docs/en/mcp
