"""Proje 56: Türkçe harf tuzakları: Claude'a yazdırılan işlevleri sınamak.

Kullanım:
    python3 main.py            # gömülü 5 yanıtı (her işten biri) sınar
Gömülü yanıtlar, yazıdaki 25 yanıttan (5 iş x 5 deneme) seçilmiş örneklerdir
(Claude Code 2.1.328, claude-opus-5-5, araçlar kapalı). Üçüncü taraf paket gerekmez.
"""
import copy
import unicodedata

BUYUK = r'''
def buyuk_harf(metin):
    return metin.replace("i", "İ").replace("ı", "I").upper()
'''

SIRALA = r'''
ALFABE = "abcçdefgğhıijklmnoöpqrsştuüvwxyz"
SIRA = {harf: i for i, harf in enumerate(ALFABE)}
SAPKALI = {"â": "a", "î": "i", "û": "u"}


def _kucult(metin):
    metin = metin.replace("I", "ı").replace("İ", "i")
    return metin.lower()


def _anahtar(isim):
    kucuk = _kucult(isim.strip())
    harfler = tuple(
        SIRA.get(SAPKALI.get(h, h), len(ALFABE) + ord(h)) for h in kucuk
    )
    return (harfler, isim)


def sirala(isimler):
    return sorted(isimler, key=_anahtar)
'''

ESLES = r'''
import unicodedata


def _turkce_kucult(metin: str) -> str:
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı")
    return unicodedata.normalize("NFC", metin.casefold())


def esles(a: str, b: str) -> bool:
    return _turkce_kucult(a) == _turkce_kucult(b)
'''

SLUG = r'''
import re
import unicodedata

_TR_HARITA = str.maketrans({
    "ç": "c", "Ç": "c",
    "ğ": "g", "Ğ": "g",
    "ı": "i", "I": "i",
    "İ": "i", "i": "i",
    "ö": "o", "Ö": "o",
    "ş": "s", "Ş": "s",
    "ü": "u", "Ü": "u",
})


def slug(baslik: str) -> str:
    if not baslik:
        return ""
    metin = unicodedata.normalize("NFC", str(baslik))
    metin = metin.translate(_TR_HARITA)
    metin = unicodedata.normalize("NFKD", metin)
    metin = "".join(k for k in metin if not unicodedata.combining(k))
    metin = metin.encode("ascii", "ignore").decode("ascii")
    metin = metin.lower()
    metin = re.sub(r"[^a-z0-9]+", "-", metin)
    return metin.strip("-")
'''

BASLIK = r'''
import re

_BUYUK_HARITA = str.maketrans({"i": "İ", "ı": "I"})
_KUCUK_HARITA = str.maketrans({"I": "ı", "İ": "i"})


def tr_buyuk(metin: str) -> str:
    return metin.translate(_BUYUK_HARITA).upper()


def tr_kucuk(metin: str) -> str:
    return metin.translate(_KUCUK_HARITA).lower()


def _kelime_duzenle(kelime: str) -> str:
    for i, harf in enumerate(kelime):
        if harf.isalpha():
            return kelime[:i] + tr_buyuk(harf) + tr_kucuk(kelime[i + 1:])
    return kelime


def baslik_yap(metin: str) -> str:
    parcalar = re.split(r"(\s+)", metin)
    return "".join(
        parca if parca.isspace() or not parca else _kelime_duzenle(parca)
        for parca in parcalar
    )
'''


def yukle(kaynak, ad):
    ns = {"__name__": "yanit"}
    exec(kaynak, ns)
    return ns[ad]


NFD = lambda s: unicodedata.normalize("NFD", s)
ISIMLER = ["Zeynep", "Çağla", "Ali", "Ömer", "Şule", "İpek", "Irmak", "Oya", "Ece",
           "Ayşe", "Gül", "Ümit", "Uğur", "Ilgaz", "ışık", "Ğ"]
SIRA = ["Ali", "Ayşe", "Çağla", "Ece", "Gül", "Ğ", "Ilgaz", "Irmak", "ışık", "İpek",
        "Oya", "Ömer", "Şule", "Uğur", "Ümit", "Zeynep"]

# (kaynak, işlev, test adı, girdi, beklenen)
TESTLER = [
    (BUYUK, "buyuk_harf", "i -> İ", ("istanbul",), "İSTANBUL"),
    (BUYUK, "buyuk_harf", "ı -> I", ("ışık ılık",), "IŞIK ILIK"),
    (BUYUK, "buyuk_harf", "karışık", ("çiğ öğüt ıspanak izmir",), "ÇİĞ ÖĞÜT ISPANAK İZMİR"),
    (SIRALA, "sirala", "alfabe sırası", (ISIMLER,), SIRA),
    (SIRALA, "sirala", "boş liste", ([],), []),
    (ESLES, "esles", "İSTANBUL ~ istanbul", ("İSTANBUL", "istanbul"), True),
    (ESLES, "esles", "ISPARTA ~ ısparta", ("ISPARTA", "ısparta"), True),
    (ESLES, "esles", "ISPARTA !~ isparta", ("ISPARTA", "isparta"), False),
    (SLUG, "slug", "İstanbul Işık Şöleni", ("İstanbul Işık Şöleni",), "istanbul-isik-soleni"),
    (SLUG, "slug", "ÇIĞLIK", ("ÇIĞLIK",), "ciglik"),
    (BASLIK, "baslik_yap", "ısparta ılık", ("ısparta ılık",), "Isparta Ilık"),
    (BASLIK, "baslik_yap", "İZMİR IŞIK", ("İZMİR IŞIK",), "İzmir Işık"),
    (BASLIK, "baslik_yap", "iNEK", ("iNEK",), "İnek"),
]
# Kenar durum: aynı metin ayrışık (NFD) biçimde: "İ" = "I" + U+0307
NFD_TESTLER = [
    (BUYUK, "buyuk_harf", (NFD("İzmir ışık"),), "İZMİR IŞIK"),
    (ESLES, "esles", (NFD("İZMİR"), "izmir"), True),
    (SLUG, "slug", (NFD("İzmir Işık"),), "izmir-isik"),
    (BASLIK, "baslik_yap", (NFD("İZMİR"),), "İzmir"),
]


def calistir(kaynak, ad, girdi):
    try:
        return yukle(kaynak, ad)(*copy.deepcopy(girdi))
    except Exception as e:  # hata da bir sonuçtur
        return f"HATA {type(e).__name__}"


def nfc(r):
    return unicodedata.normalize("NFC", r) if isinstance(r, str) else r


def duzelt_baslik(kaynak):
    """baslik_yap'ın başına NFC normalleştirmesi ekler (tek satırlık düzeltme)."""
    return kaynak.replace(
        "def baslik_yap(metin: str) -> str:\n",
        "def baslik_yap(metin: str) -> str:\n    metin = __import__('unicodedata').normalize('NFC', metin)\n",
    )


if __name__ == "__main__":
    gecen = 0
    print("Düz (NFC) girdi:")
    for kaynak, ad, test, girdi, beklenen in TESTLER:
        r = calistir(kaynak, ad, girdi)
        ok = r == beklenen
        gecen += ok
        print(f"  {'GEÇTİ' if ok else 'KALDI'}  {ad:11} {test}" + ("" if ok else f"  -> {r!r}"))
    print(f"  {gecen}/{len(TESTLER)}\n")

    print("Ayrışık (NFD) girdi:")
    for kaynak, ad, girdi, beklenen in NFD_TESTLER:
        r = nfc(calistir(kaynak, ad, girdi))
        ok = r == beklenen
        print(f"  {'GEÇTİ' if ok else 'KALDI'}  {ad:11} {unicodedata.normalize('NFC', girdi[0])!r}" + ("" if ok else f"  -> {r!r}"))

    print("\nbaslik_yap + NFC düzeltmesi:")
    r = calistir(duzelt_baslik(BASLIK), "baslik_yap", (NFD("İZMİR"),))
    print(f"  {nfc(r)!r}  ({'GEÇTİ' if nfc(r) == 'İzmir' else 'KALDI'})")
