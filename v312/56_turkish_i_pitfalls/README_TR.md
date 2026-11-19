# Proje 56: Türkçe İ ve ı: Claude'un Yazdığı İşlevleri Sınamak

Claude'a (Claude Code 2.1.328, `claude-opus-5-5`, araçlar kapalı) on iki küçük Türkçe metin işi beşer kez yazdırıldı: büyük harfe çevirme, alfabetik sıralama, büyük/küçük harf yok sayarak eşleştirme, slug, başlık biçimi, kelime sayımı, önek arama, kullanıcı adı. 60 yanıt üç turda 260 testten geçti: 260/260. Aynı metin ayrışık (NFD) Unicode biçiminde verilince `baslik_yap` 10 yanıtın 10'unda `İzmir` yerine `İzmı̇r` döndürdü: `I` + U+0307 dizisindeki `I` küçülürken `ı` oluyor ve birleştirici nokta üstünde kalıyor.

Bu betik her işten bir yanıtı gömülü olarak içerir (60 yanıtın tamamı değil; tamamı blog yazısının klasöründe). 13 düz ve 4 ayrışık girdi testini çalıştırır, sonra `baslik_yap`'a tek satırlık NFC düzeltmesini uygular.

| Sınama | Test | Geçen |
|---|---|---|
| 1. tur: istemde "Türkçe" yazılı (5 iş) | 115 | 115 |
| 2. tur: yalnızca Türkçe örnek veri (4 iş) | 90 | 90 |
| 3. tur: Türkçe işin kenarında (3 iş) | 55 | 55 |
| Ayrışık `İ`: `buyuk_harf`, `esles`, `slug` | 25 | 25 |
| Ayrışık `İ`: `baslik_yap` | 10 | 0 |

## Nasıl Çalışır?
- Her yanıt `exec` ile ayrı bir ad alanında yüklenir; girdiler `deepcopy` ile verilir, istisnalar sonuç olarak gösterilir.
- Beklenenler Türkçe kurallarına göre yazıldı. En tartışmalısı: `esles("ISPARTA", "isparta")` Türkçe'de `ı` ile `i` farklı harf olduğu için `False` bekleniyor.
- Ayrışık test, aynı metni `unicodedata.normalize("NFD", ...)` ile ayrıştırıp çıktıyı karşılaştırmadan önce NFC'ye çevirir.
- `duzelt_baslik` işlevin başına `unicodedata.normalize("NFC", metin)` ekler.

## Sınırlar
- Tek model, tek sürüm; istemlerde "hiç ipucu olmayan" durum denenmedi.
- Ayrışık sınama yalnızca 1. ve 2. turun dört işlevinde yapıldı.
- Test beklentileri yazarın tercihidir; 3. turda bir testi (`izmir` sayısı) hatalı yazdığımız için çıkarıldı.

## Proje Yapısı
```text
56_turkish_i_pitfalls/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü. Python 3.12.3 ile ve Docker'da 3.9 ve 3.14 ile test edildi; çıktı aynı.
- Üçüncü taraf paket gerekmiyor.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
Düz (NFC) girdi:
  GEÇTİ  buyuk_harf  i -> İ
  GEÇTİ  buyuk_harf  ı -> I
  GEÇTİ  buyuk_harf  karışık
  GEÇTİ  sirala      alfabe sırası
  GEÇTİ  sirala      boş liste
  GEÇTİ  esles       İSTANBUL ~ istanbul
  GEÇTİ  esles       ISPARTA ~ ısparta
  GEÇTİ  esles       ISPARTA !~ isparta
  GEÇTİ  slug        İstanbul Işık Şöleni
  GEÇTİ  slug        ÇIĞLIK
  GEÇTİ  baslik_yap  ısparta ılık
  GEÇTİ  baslik_yap  İZMİR IŞIK
  GEÇTİ  baslik_yap  iNEK
  13/13

Ayrışık (NFD) girdi:
  GEÇTİ  buyuk_harf  'İzmir ışık'
  GEÇTİ  esles       'İZMİR'
  GEÇTİ  slug        'İzmir Işık'
  KALDI  baslik_yap  'İZMİR'  -> 'İzmı̇r'

baslik_yap + NFC düzeltmesi:
  'İzmir'  (GEÇTİ)
```
