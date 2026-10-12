# Proje 23: Yapısal Desen Eşleme (match-case)

`if`/`elif` zinciri yerine `match`/`case` kullanan küçük bir komut işleyici. `process_command()` fonksiyonu farklı biçimlerde girdiler alır (bir metin, listeler, `Order` veri sınıfı nesneleri, bir sözlük) ve girdinin yapısına ve türlerine göre bir dal seçer.

| # | Desen türü | Koddaki örnek |
|---|------------|---------------|
| 1 | Sabit değer deseni | `case "EXIT":` |
| 2 | Tür kontrollü dizi deseni | `case ["add", str(item), int(qty)]:` |
| 3 | Koşullu (guard) yıldız deseni | `case ["delete", *id_list] if len(id_list) > 0:` |
| 4 | Sınıf deseni (anahtar kelimeli öznitelikler) | `case Order(product_name=name, quantity=qty, status="shipped"):` |
| 5 | `as` ile bağlanan sınıf deseni | `case Order() as order:` |
| 6 | Sözlük (mapping) deseni | `case {"type": "invoice", "amount": float(amt)}:` |
| 7 | Joker (her şeyi yakalayan) | `case _:` |

## Proje Yapısı
```text
23_structural_pattern_matching/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.10 veya üstü (`match`/`case` 3.10'da eklendi, PEP 634). 3.12.3 ile test edildi; 3.10 ve 3.11'de de çalışır.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
--- Python Match-Case Test Started ---

Input: ['add', 'Laptop', 2]
Stock updated: Added 2 units of 'Laptop'.
---------------------------------------------
Input: ['delete', 404, 505]
Deleting products with IDs: [404, 505]
---------------------------------------------
Input: Order(product_name='Wireless Headphones', quantity=1, status='shipped')
In-Transit: Wireless Headphones (1 units) is currently with the carrier.
---------------------------------------------
Input: Order(product_name='Coffee Maker', quantity=1, status='pending')
General Order Info: Coffee Maker - Status: pending
---------------------------------------------
Input: {'type': 'invoice', 'amount': 1250.5}
Invoice processed. Amount: $1250.50
---------------------------------------------
Input: ['invalid_command_format']
Invalid or unrecognized command format: ['invalid_command_format']
---------------------------------------------
Input: EXIT
Exiting system...
---------------------------------------------
```

## Nasıl Çalışır?
- `case` blokları yukarıdan aşağıya denenir; ilk eşleşen çalışır. Bu yüzden `Order(..., status="shipped")` deseni genel `Order()` deseninden önce gelir.
- `str(item)` ve `int(qty)` hem türü kontrol eder hem de değeri değişkene bağlar. `["add", "Laptop", "2"]` (miktar metin olarak) eşleşmez ve `case _` dalına düşer.
- Dizi deseni listelerle ve demetlerle (tuple) eşleşir, metinlerle asla eşleşmez. `("add", "Laptop", 2)` de `add` dalına girer.
- `*id_list` kalan öğeleri toplar; `if len(id_list) > 0` koşulu tek başına `["delete"]` girdisini reddeder.
- Sözlük deseni yalnızca yazılan anahtarlara bakar; fazladan anahtarlar yok sayılır. `float(amt)` yüzünden `{"type": "invoice", "amount": 1250}` gibi tam sayı bir tutar eşleşmez.
- `process_command()` yalnızca `"EXIT"` için `False` döndürür ve döngü durur.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/02/pythonda-modern-veri-ayristirma-yapisal-pattern-matching-match-case/
- `match` ifadesi belgeleri: https://docs.python.org/3/reference/compound_stmts.html#the-match-statement
- PEP 636: Yapısal desen eşleme öğreticisi: https://peps.python.org/pep-0636/
