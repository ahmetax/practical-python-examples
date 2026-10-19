# Proje 46: Kuyruk Bekçisi — WordPress Yayın Kuyruğu Zayıflayınca Uyarı

gurmezin.com'da bir kural var: sitede her zaman en az bir zamanlanmış yazı bulunur. Bu betik kuralı her saat başı denetliyor. Zamanlanmış (`status=future`) yazıları WordPress REST API'den okuyor, kuyruğu dört durumdan birine yerleştiriyor ve TAMAM dışındaki her durumda masaüstü bildirimi gönderiyor.

| Durum | Ne zaman? | Çıkış kodu |
|-------|-----------|------------|
| TAMAM | En az iki zamanlanmış yazı var ve sıradaki yayın günü (Pzt/Per 10:00) dolu | 0 |
| UYARI | Tek yazı kaldı ya da sıradaki yayın günü boş | 1 |
| KRİTİK | Hiç zamanlanmış yazı yok ya da saati 30 dakikadan fazla geçtiği hâlde yayınlanmamış yazı var | 2 |
| HATA | Kuyruk okunamadı (ağ, yetki, sunucu) | 3 |

Bekçi 15.10.2026'da kuruldu. 19.10.2026'da iki açığı kapatıldı:

1. Sunucu bağlantıyı yanıtsız kapattığında (`RemoteDisconnected`) betik çöküyordu: günlüğe kayıt yok, bildirim yok. İlk sürümdeki `except` satırı yalnızca `URLError` ve `TimeoutError`'ı yakalıyordu. Bağlantı kurulduktan sonra oluşan hatalar ise `OSError` ya da `http.client.HTTPException` olarak sarılmadan geliyor.
2. WordPress'in saatinde yayınlayamadığı bir yazı ("Missed schedule") TAMAM sayılıyordu, çünkü bekçi yalnızca sonraki yayın günlerine bakıyordu.

`--demo` seçeneği bu iki açığı sunucu ve kimlik bilgisi olmadan gösteriyor.

## Proje Yapısı
```text
46_queue_watchdog/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü (`list[dict]` tip ipucu). Python 3.12.3 (Ubuntu 24.04) ve Docker'da `python:3.9-slim` (`--network none`, yalnızca `--demo`) ile test edildi. 3.8'de `TypeError: 'type' object is not subscriptable` veriyor.
- Yalnızca standart kütüphane.
- Gerçek denetim için: WordPress uygulama parolası ve `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` ortam değişkenleri. Bildirim için `notify-send` (Ubuntu'da `libnotify-bin`).
- Yayın günleri ve saati kodun başında (`YAYIN_GUNLERI`, `YAYIN_SAATI`). Mesajlar Türkçe.

## Çalıştırma
```bash
python3 main.py --demo    # çevrimdışı gösterim
python3 main.py           # günde bir kez denetle (aynı gün aynı durum kayıtlıysa sessizce çıkar)
python3 main.py --zorla   # bugün kayıtlı olsa da denetle
```

Denetim sonuçları `main.py`'nin yanındaki `kuyruk_bekcisi.log` dosyasına JSON satırları olarak eklenir. `--demo` dosya yazmaz.

Cron örneği (her saatin 5. dakikası). Bilgisayar sabah kapalı olsa da denetim ilk açık saatte yapılır:

```text
5 * * * * /bin/bash -ic 'python3 /yol/main.py' 2>&1 >/dev/null | grep -v -e 'no job control' -e 'terminal process group' >> /yol/kuyruk_bekcisi.err
```

`bash -ic`, kimlik bilgileri `~/.bashrc` içindeyse gerekiyor: Ubuntu'nun `.bashrc` dosyası etkileşimli olmayan kabukta ilk satırlarda çıkıyor. `grep -v` satırı, terminalsiz etkileşimli kabuğun her seferinde bastığı uyarıları süzüyor. Yakalanmayan bir hata olursa izi `.err` dosyasında kalır.

## Örnek Çıktı (`--demo`, Python 3.12.3, Ubuntu 24.04)
```text
== Queue scenarios ==
  Normal, three posts                TAMAM   3 zamanlanmış yazı, en sonuncusu 26.10 10:00.
  Only one post left                 UYARI   Kuyrukta tek yazı kaldı (26.10). Sıradakini hazırlayın.
  Next Thursday is empty             UYARI   Sıradaki yayın günü (22.10 Perşembe) boş. 2 zamanlanmış yazı, en sonuncusu 29.10 10:00.
  Queue empty                        KRİTİK  Kuyrukta hiç zamanlanmış yazı yok.
  Scheduled at 09:00 by mistake      UYARI   Sıradaki yayın günü (22.10 Perşembe) boş. 2 zamanlanmış yazı, en sonuncusu 26.10 10:00.
  10:00 post still future at 11:00   KRİTİK  Saati geçtiği hâlde yayınlanmamış yazı var (22.10 10:00). WP-Cron'u kontrol edin.

== Network errors: caught as HATA, or crash? ==
  exception              15.10 except   19.10 except
  URLError               HATA           HATA
  TimeoutError           HATA           HATA
  JSONDecodeError        HATA           HATA
  RemoteDisconnected     CRASH          HATA
  ConnectionResetError   CRASH          HATA
  IncompleteRead         CRASH          HATA
```

Gerçek denetimden bir satır (`--zorla`, 19.10.2026):

```text
TAMAM: 2 zamanlanmış yazı, en sonuncusu 26.10 10:00.
```

## Sınırlamalar
- Site saati ile bilgisayar saatinin aynı saat diliminde olduğu varsayılıyor (WordPress `date` alanı site saatiyle döner).
- 30 dakikalık gecikme payı (`GECIKME_PAYI`) içinde takılan bir yazı henüz alarm vermez. Bu, WP-Cron'un yayını birkaç dakika geciktirmesinin yanlış alarm üretmemesi için.
- Günlükteki bozuk bir JSON satırı `bugun_kaydedildi()` içinde hataya yol açar.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/10/29/claude-ile-otomasyon-4-yayin-kuyruguna-bekci-koyduk/
- WordPress REST API, yazılar: https://developer.wordpress.org/rest-api/reference/posts/
- `http.client` istisnaları: https://docs.python.org/3/library/http.client.html#http.client.RemoteDisconnected
- `urllib.error`: https://docs.python.org/3/library/urllib.error.html
