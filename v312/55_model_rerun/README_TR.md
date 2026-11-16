# Proje 55: Modeller İyileşiyor mu? Aynı Üç İş, Ağustos ve Bugün

31 (merge sort), 32 (ikili arama ağacı) ve 38 (regex doğrulayıcıları) numaralı projeleri Ağustos ve Eylül'de bir yapay zekâ yazdı. Sonraki yazılarda bu kodlarda, örnek girdilerin göstermediği sorunlar bulduk. Burada aynı üç iş bugünkü modele yeniden verildi (Claude Code 2.1.325, `claude-opus-5-5`, araçlar kapalı, her iş için beş deneme). Betik, eski kodu ve bugünkü yanıtlardan birini aynı 23 testle sınıyor.

| Alan | Eski kod ("says") | Bugünkü beş yanıt ("model") |
|---|---|---|
| Merge sort: kararlılık, 0/1 elemanda yeni liste | 3 testten kalıyor | 5/5 yanıtta düzeldi |
| Ağaç: 1000'in üstünde sıralı ekleme | `RecursionError` | 5/5 yanıtta çökmüyor (özyineleme yerine döngü) |
| Ağaç: yinelenen değerler | korunuyor (`[3, 3, 5, 5, 8]`) | 5/5 yanıtta sessizce atılıyor (`[3, 5, 8]`) |
| Şifre denetimi ve Türkçe harfler | `[A-Z]` `Ş` ve `İ`'yi görmüyor | 5/5 yanıtta düzeldi |
| Telefon: Arapça-Hint rakamlar (`\d`) | kabul ediliyor | 5/5 yanıtta hâlâ kabul ediliyor |
| Telefon: sondaki satır sonu (`strip()`) | kabul ediliyor | 5/5 yanıtta hâlâ kabul ediliyor |
| Telefon: gruplar arasında satır sonu / bölünmez boşluk (`\s?`) | kabul ediliyor | 3/5 yanıtta kabul ediliyor |
| E-posta: sondaki satır sonu | kabul ediliyor | 1/5 yanıtta kabul ediliyor (`fullmatch` öncesinde `strip()`) |

Eski kodun kaldığı 13 testin 7'si beş yanıtın hepsinde düzelmiş, 6'sı en az bir yanıtta hâlâ kalıyor. Yinelenen değer testi yeni: eski kod bu testi geçiyor.

## Nasıl Çalışır?
- Üç istem `PROMPTS` içinde (gerçek istemler Türkçeydi, blog yazısında var). İstemlerde doğrulamadan, sınırlardan ya da güvenlikten söz edilmiyor.
- `SAYS_*`, 31, 32 ve 38 numaralı projelerin özgün kodunu (işlevler değiştirilmeden kopyalandı) içeriyor. `MODEL_*`, bugünkü yanıtlardan birini içeriyor: regex için 4. yanıt, merge sort ve ağaç için 1. yanıt. Yukarıdaki tablodaki sayımlar her işin beş yanıtının tamamı üzerinden ve blog yazısından geliyor.
- Her yanıt `exec` ile `__name__ == "answer"` altında yükleniyor, böylece kendi deneme bloğu çalışmıyor. Yanıtın yazdırdıkları atılıyor. İstisnalar (`RecursionError` dahil) test ayrıntısına dönüşüyor.
- Özyineleme sınırı çıktı tekrarlanabilsin diye 1000'e (varsayılan) ayarlı. Ağaçtaki son test sıralı ve karışık ekleme sürelerini karşılaştırıyor, yani bu iki sayı makineden makineye değişir.
- Başka bir yanıtı sınamak için: `python3 main.py regex yanit.py` (`regex`, `sort` ya da `tree`).

## Sınırlar
- Testler, eski kodda zaten bulunmuş sorunlardan çıkıyor. Bugünkü yanıtlarda başka sorunlar olabilir. Yinelenen değer davranışı yanıtları okurken bulundu.
- Tek model, her iş için tek istem, beşer deneme.

## Proje Yapısı
```text
55_model_rerun/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü. Python 3.12.3 ile ve Docker'da 3.9 ve 3.14 ile test edildi; süre sayıları dışında çıktı aynı.
- Üçüncü taraf paket gerekmiyor.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
== regex ==
  test                                             says   model  detail (model)
  email: normal address accepted                   pass   pass
  email: trailing newline rejected                 FAIL   pass
  email: 'user@com' rejected                       pass   pass
  phone: normal formats accepted                   pass   pass
  phone: Arabic-Indic digits rejected              FAIL   FAIL   True
  phone: newlines between groups rejected          FAIL   FAIL   True
  phone: trailing newline rejected                 FAIL   FAIL   True
  phone: no-break spaces rejected                  FAIL   FAIL   True
  password: 'Şifre123!x' is strong                 FAIL   pass
  password: 'çğışöü12!A' is strong                 FAIL   pass
  password: 'ŞİFRE123!' lacks lowercase            pass   pass
  password: 'şifre123!x' lacks uppercase           pass   pass

== sort ==
  test                                             says   model  detail (model)
  1000 random lists == sorted()                    pass   pass
  equal keys keep their order (stable)             FAIL   pass
  one element: a new list comes back               FAIL   pass
  zero elements: a new list comes back             FAIL   pass
  20000 reversed elements                          pass   pass

== tree ==
  test                                             says   model  detail (model)
  1000 shuffled inserts: search + in-order         pass   pass
  900 sorted inserts without a crash               pass   pass
  1000 sorted inserts without a crash              FAIL   pass
  5000 sorted inserts without a crash              FAIL   pass
  duplicates: in-order == sorted([5,3,5,8,3])      pass   FAIL   [3, 5, 8]
  3000 sorted inserts < 10x the shuffled time      FAIL   FAIL   sorted 835 ms, shuffled 10 ms
```

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/12/03/modeller-iyilesiyor-mu-agustos-projeleri-claude-yeniden-yazdirdik/
- Özgün projeler: `v312/31_custom_sorting_algorithms`, `v312/32_data_structures_bin_tree`, `v312/38_regex_validation`
- Önceki bulgular: `v312/47_regex_edge_cases`, `v312/51_tested_but_wrong`, `v312/53_lenient_api`
- Python `re` belgeleri: https://docs.python.org/3/library/re.html
