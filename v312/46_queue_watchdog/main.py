# Author: Ahmet Aksoy & Claude
# Date: 19.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.9+ (list[dict] annotations)

"""
Queue Watchdog: Alerting When a WordPress Publishing Queue Runs Low
Reads the scheduled (status=future) posts through the WordPress REST API and
classifies the queue as TAMAM (ok), UYARI (warning), KRİTİK (critical) or
HATA (could not read). Anything but TAMAM triggers a desktop notification.
A read error is a state of its own: a watchdog that cannot see must not stay silent.

Cron calls it every hour; it logs one JSON line per day unless the state changes.
Credentials come from WP_URL, WP_USER and WP_APP_PASSWORD.

    python3 main.py           # check once a day (cron)
    python3 main.py --zorla   # check now even if today's state is logged
    python3 main.py --demo    # offline: queue scenarios and network error test

Exit codes: 0 TAMAM, 1 UYARI, 2 KRİTİK, 3 HATA
"""
import base64
import http.client
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

GUNLUK = Path(__file__).with_name("kuyruk_bekcisi.log")
YAYIN_GUNLERI = (0, 3)  # Pazartesi, Perşembe
YAYIN_SAATI = 10
GUN_ADLARI = ("Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar")
KODLAR = {"TAMAM": 0, "UYARI": 1, "KRİTİK": 2, "HATA": 3}
# WP-Cron zamanlanmış yazıyı ancak siteye bir istek gelince yayınlar; birkaç dakikalık gecikme normaldir
GECIKME_PAYI = timedelta(minutes=30)


def kuyrugu_oku() -> list[dict]:
    url = os.environ["WP_URL"].rstrip("/") + \
        "/wp-json/wp/v2/posts?status=future&per_page=100&orderby=date&order=asc&_fields=id,date,title"
    yetki = base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": "Basic " + yetki,
                                               "User-Agent": "gurmezin-kuyruk-bekcisi/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        veri = json.loads(r.read())
    if not isinstance(veri, list):  # yetki hatasında WP bir sözlük döndürür
        raise ValueError(f"beklenmeyen yanıt: {str(veri)[:200]}")
    return veri


def siradaki_yayin(simdi: datetime) -> datetime:
    """Şu andan sonraki ilk Pazartesi/Perşembe 10:00 (site saati = yerel saat)."""
    aday = simdi.replace(hour=YAYIN_SAATI, minute=0, second=0, microsecond=0)
    while aday <= simdi or aday.weekday() not in YAYIN_GUNLERI:
        aday = (aday + timedelta(days=1)).replace(hour=YAYIN_SAATI)
    return aday


def degerlendir(yazilar: list[dict], simdi: datetime) -> tuple[str, str]:
    if not yazilar:
        return "KRİTİK", "Kuyrukta hiç zamanlanmış yazı yok."
    tarihler = [datetime.fromisoformat(y["date"]) for y in yazilar]
    kacan = [t for t in tarihler if t < simdi - GECIKME_PAYI]
    if kacan:
        return "KRİTİK", f"Saati geçtiği hâlde yayınlanmamış yazı var ({min(kacan):%d.%m %H:%M}). WP-Cron'u kontrol edin."
    hedef = siradaki_yayin(simdi)
    ozet = f"{len(yazilar)} zamanlanmış yazı, en sonuncusu {max(tarihler):%d.%m %H:%M}."
    if hedef not in tarihler:
        return "UYARI", f"Sıradaki yayın günü ({hedef:%d.%m} {GUN_ADLARI[hedef.weekday()]}) boş. {ozet}"
    if len(yazilar) == 1:
        return "UYARI", f"Kuyrukta tek yazı kaldı ({tarihler[0]:%d.%m}). Sıradakini hazırlayın."
    return "TAMAM", ozet


def bugun_kaydedildi(durum: str, bugun: str) -> bool:
    try:
        satirlar = GUNLUK.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return False
    for satir in reversed(satirlar):
        k = json.loads(satir)
        if k["zaman"].startswith(bugun):
            return k["durum"] == durum
    return False


def bildir(durum: str, mesaj: str) -> bool:
    ortam = dict(os.environ)
    ortam.setdefault("DBUS_SESSION_BUS_ADDRESS", f"unix:path=/run/user/{os.getuid()}/bus")
    aciliyet = "normal" if durum == "UYARI" else "critical"
    try:
        r = subprocess.run(["notify-send", "-u", aciliyet, "-a", "gurmezin",
                            f"gurmezin kuyruğu: {durum}", mesaj],
                           env=ortam, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"Bildirim gönderilemedi: {exc}", file=sys.stderr)
        return False
    if r.returncode != 0:
        print(f"Bildirim gönderilemedi: {r.stderr.strip()}", file=sys.stderr)
    return r.returncode == 0


def main() -> int:
    simdi = datetime.now().replace(microsecond=0)
    try:
        yazilar = kuyrugu_oku()
        durum, mesaj = degerlendir(yazilar, simdi)
    # URLError, TimeoutError ve bağlantı kopmaları OSError'dan; IncompleteRead ve
    # RemoteDisconnected HTTPException'dan türer. Yakalanmayan hata cron'da sessizce kaybolur.
    except (OSError, http.client.HTTPException, ValueError, KeyError) as exc:
        yazilar, durum, mesaj = [], "HATA", f"Kuyruk okunamadı: {exc}"

    if "--zorla" not in sys.argv and bugun_kaydedildi(durum, simdi.date().isoformat()):
        return KODLAR[durum]

    print(f"{durum}: {mesaj}")
    kayit = {"zaman": simdi.isoformat(), "durum": durum, "sayi": len(yazilar),
             "tarihler": [y["date"] for y in yazilar], "mesaj": mesaj}
    if durum != "TAMAM":
        kayit["bildirim"] = bildir(durum, mesaj)
    with GUNLUK.open("a", encoding="utf-8") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
    return KODLAR[durum]


# --- Çevrimdışı gösterim (--demo): sunucu ve kimlik bilgisi gerekmez ------------------
ILK_SURUM = (urllib.error.URLError, TimeoutError, ValueError, KeyError)  # 15.10.2026
DUZELTME = (OSError, http.client.HTTPException, ValueError, KeyError)   # 19.10.2026


def demo() -> int:
    def kuyruk(*tarihler):
        return [{"date": t} for t in tarihler]

    senaryolar = [
        ("Normal, three posts", "2026-10-19T08:00",
         kuyruk("2026-10-19T10:00:00", "2026-10-22T10:00:00", "2026-10-26T10:00:00")),
        ("Only one post left", "2026-10-23T09:00", kuyruk("2026-10-26T10:00:00")),
        ("Next Thursday is empty", "2026-10-19T11:00",
         kuyruk("2026-10-26T10:00:00", "2026-10-29T10:00:00")),
        ("Queue empty", "2026-10-19T11:00", []),
        ("Scheduled at 09:00 by mistake", "2026-10-19T11:00",
         kuyruk("2026-10-22T09:00:00", "2026-10-26T10:00:00")),
        ("10:00 post still future at 11:00", "2026-10-22T11:00",
         kuyruk("2026-10-22T10:00:00", "2026-10-26T10:00:00", "2026-10-29T10:00:00")),
    ]
    print("== Queue scenarios ==")
    for ad, simdi, yazilar in senaryolar:
        durum, mesaj = degerlendir(yazilar, datetime.fromisoformat(simdi))
        print(f"  {ad:34} {durum:7} {mesaj}")

    hatalar = [
        urllib.error.URLError("[Errno -2] Name or service not known"),
        TimeoutError("The read operation timed out"),
        json.JSONDecodeError("Expecting value", "<html>", 0),
        http.client.RemoteDisconnected("Remote end closed connection without response"),
        ConnectionResetError(104, "Connection reset by peer"),
        http.client.IncompleteRead(b"[{"),
    ]
    print("\n== Network errors: caught as HATA, or crash? ==")
    print(f"  {'exception':22} {'15.10 except':14} 19.10 except")
    for hata in hatalar:
        ilk = "HATA" if isinstance(hata, ILK_SURUM) else "CRASH"
        yeni = "HATA" if isinstance(hata, DUZELTME) else "CRASH"
        print(f"  {type(hata).__name__:22} {ilk:14} {yeni}")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
