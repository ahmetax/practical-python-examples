# Proje 28: Düzenli İfadelerle Log Satırlarını Ayrıştırma

Düz metin log satırlarını tek bir düzenli ifadeyle Python sözlüklerine dönüştürür. Yalnızca standart `re` ve `json` modüllerini kullanır.

| Teknik | Kullanıldığı yer |
|--------|------------------|
| İsimli gruplar `(?P<ad>...)` ve `match.groupdict()` | `parse_system_logs()` |
| `^` ve `$` her satırda eşleşsin diye `re.MULTILINE` | iki fonksiyonda da |
| `[code:NNN]` eki için isteğe bağlı grup `(?:...)?` | `parse_system_logs()` |
| Mesaj kodu da yutmasın diye tembel niceleyici `.+?` | `parse_system_logs()` |
| İleriye bakma `(?=...)` ve `re.IGNORECASE` | `extract_critical_failures_with_lookahead()` |

## Nasıl Çalışır?
Her log satırı şu biçimdedir:
```text
[2026-05-22 08:30:15,123] [ERROR] [auth.service] (192.168.1.50) - Invalid credentials provided [code:401]
```
- `parse_system_logs()` metni `finditer()` ile tarar ve her eşleşmeyi `timestamp`, `level`, `component`, `ip_address`, `message` ve `status_code` anahtarlı bir sözlüğe çevirir. `status_code` değeri `int` türüne dönüştürülür; satırda `[code:...]` kısmı yoksa `None` olur.
- `extract_critical_failures_with_lookahead()` içinde herhangi bir yerde `[database]` geçen ve ayrıca `denied` ya da `failed` kelimesini (büyük/küçük harf fark etmeden) içeren satırları olduğu gibi döndürür. Örnek veride iki koşulu birden sağlayan tek satır vardır; `payment.gateway` satırında `failed` geçer ama bu bir veritabanı satırı değildir.

Bilinmesi gereken sınırlar (fonksiyonlar ek girdilerle çalıştırılarak denendi):
- Desene uymayan satırlar sessizce atlanır. Örneğin `[DEBUG]` izin verilen seviyeler arasında değildir (`INFO|WARNING|ERROR|CRITICAL`) ve sonuçta hiç görünmez.
- IP deseni `\d{1,3}(?:\.\d{1,3}){3}` yalnızca biçime bakar; `999.300.1.1` de kabul edilir.
- Windows satır sonlarında (`\r\n`) `$`, `\r` karakterinden sonra eşleşir ve kod grubu artık uymaz: mesaj `'Invalid credentials provided [code:401]\r'` olur, `status_code` ise `None` kalır. Böyle dosyaları ayrıştırmadan önce `splitlines()` kullanın ya da `\r` karakterlerini temizleyin.
- İleriye bakma, `[database]` ifadesini satırın her yerinde arar; mesajında `[database]` geçen bir satır da eşleşir.

## Proje Yapısı
```text
28_regex_mastery/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü (`list[dict]` tip ipuçları 3.9 gerektirir). Python 3.12.3 (Ubuntu 24.04) ile test edildi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
--- Advanced Regex Analytical Engine Started ---

=== 1. Parsing Full Log Stack via Named Capture Groups ===
[
  {
    "timestamp": "2026-05-22 08:30:12,001",
    "level": "INFO",
    "component": "web.server",
    "ip_address": "192.168.1.10",
    "message": "Connection established successfully",
    "status_code": null
  },
  {
    "timestamp": "2026-05-22 08:30:15,123",
    "level": "ERROR",
    "component": "auth.service",
    "ip_address": "192.168.1.50",
    "message": "Invalid credentials provided",
    "status_code": 401
  }
]
Total structured log profiles extracted: 6
-----------------------------------------------------------------

=== 2. Filtering Specific Contexts using Lookaheads ===
Targeting lines matching 'database' containing failures ('denied' / 'failed'):
  Match #1: [2026-05-22 08:31:05,890] [CRITICAL] [database] (10.0.0.5) - Access denied for user 'admin_app' [code:1045]
-----------------------------------------------------------------
```
Ayrıştırılan altı kaydın yalnızca ilk ikisi yazdırılır.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/22/pythonda-regex-ustalik-sinifi-karmasik-log-dosyalarini-duzenli-veriye-donusturmek/
- `re` belgeleri: https://docs.python.org/3/library/re.html
- Düzenli İfade Rehberi (Regular Expression HOWTO): https://docs.python.org/3/howto/regex.html
