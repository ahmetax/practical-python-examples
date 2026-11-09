# Proje 52: Tek Yazma Araçlı, Korumalı MCP Sunucusu (WordPress Taslakları)

Salt okunur MCP sunucusu olan [proje 49](../49_mcp_queue_server/)'un devamı. Bu sunucu tek bir yazma aracı, `upload_draft`, ekliyor ve önüne birkaç koruma koyuyor. En önemlisi: **onay modelden değil, kullanıcıdan gelir.** Sunucu, soruyu MCP istemcisi üzerinden kullanıcıya sorar (elicitation). Modele verilen bir onay kodu insan onayı değildir, çünkü model kodu kendisi iletebilir.

| Koruma | Ne yapar? |
|--------|-----------|
| Varsayılan kuru çalıştırma | `dry_run=True` hiçbir şey yazmaz; özeti ve bulunan sorunları döndürür |
| İnsan onayı | `dry_run=False`: sunucu istemci üzerinden kullanıcıya sorar; cevap yoksa, `decline` ya da `cancel` ise hiçbir şey yazılmaz |
| Sabit durum | Yazılar her zaman `status=draft` olarak oluşturulur; zamanlama ve yayın parametre değildir |
| Dar kapsam | Yalnızca `POSTS_DIR/<klasör>/post.json`; güncelleme ve silme yok; kullanılmış slug, dolu gün (zamanlanmış **ya da taslak**) ya da Pazartesi/Perşembe 10:00 dışındaki tarih reddedilir; eksik kategori/etiket oluşturulmaz |
| Sınır ve iz | Sunucu süreci başına en çok 2 yazma; her deneme, anlaşılan protokol sürümüyle birlikte `draft_log.jsonl`'e yazılır |

Bir de salt okunur `publish_queue` aracı var.

## Proje Yapısı
```text
52_mcp_draft_guard/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.10 veya üstü ve `mcp>=2,<3`. Python 3.12.3, `mcp` 2.3.0 ve Claude Code 2.1.319 ile Ubuntu 24.04'te test edildi.
- Gerçek bir site için `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` değişkenlerinde bir WordPress uygulama şifresi. `--demo` ve `--check` hiçbir şey gerektirmez.

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp>=2,<3"
```

## Çalıştırma
```bash
.venv/bin/python main.py --check   # sahte siteyle sunucuyu istemci olarak başlatır, onay senaryolarını çalıştırır
.venv/bin/python main.py --demo    # bellekte duran sahte siteyle stdio sunucusu
.venv/bin/python main.py           # gerçek site için stdio sunucusu
```

Bir yazı klasörü (varsayılan `POSTS_DIR`: `./posts`) şöyle görünür. Metin düz paragraflar olarak gönderilir:
```json
{"title": "Yazım", "slug": "yazim", "date": "2026-11-23T10:00:00", "markdown": "post.md",
 "excerpt": "Kısa özet.", "categories": ["python"], "tags": ["mcp"]}
```

## Örnek Çıktı (`--check`, Python 3.12.3, mcp 2.3.0)
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
Tarihler, betiği çalıştırdığınız güne göre değişir. Sahte site bellekte durduğu için her oturum boş başlar.

## Denemelerden Notlar
- **`ctx.elicit()` Claude Code'da çalışmadı.** `mcp` Python istemcisi `2025-11-25` protokolüyle bağlandı; bu sürümde sunucu, araç çalışırken `elicitation/create` isteği gönderir. Claude Code 2.1.319 ise `2026-07-28` ile bağlandı; bu sürümde sunucu bir `InputRequiredResult` döndürür, istemci cevabı alıp aracı yeniden çağırır. `ctx.elicit()` `NoBackChannelError` verdi. `Elicit(...)` döndüren bir çözücü (`Annotated[..., Resolve(fn)]`) iki sürümde de çalışır.
- **`claude -p` kipinde soru gösterilemiyor.** Claude Code `cancel` cevabı verdi ve hiçbir şey yazılmadı; istemde "bana sormana gerek yok" yazdığında da.
- **İki adımlı onay kodu yetmedi.** İstemde "bana sormana gerek yok" olduğunda model kodu ikinci araca kendisi verdi.
- **İzin kipleri ayrı bir katman.** Claude Code'un `auto` kipinde yazma aracı, `read_only_hint=False` olmasına rağmen izin sorulmadan çağrıldı; yazmayı yalnızca sunucunun kendi onay sorusu durdurdu.
- **Uygulama şifresi, kullanıcısının bütün yetkilerini taşır.** Sunucuyu WordPress'te "Katılımcı" (Contributor) rolündeki bir kullanıcıyla çalıştırmak, WordPress tarafında bir koruma daha ekler (burada yapılmadı).
- Claude Code'da bir `Elicitation` kancası (hook) soruyu göstermeden cevaplayabilir. Bu model davranışı değil kullanıcı ayarıdır, ama akılda tutun.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/11/23/mcp-sunucusuna-yazma-araci-onayi-kullaniciya-sordurduk/
- MCP belirtimi 2026-07-28, Elicitation: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- Claude Code MCP belgeleri: https://code.claude.com/docs/en/mcp
