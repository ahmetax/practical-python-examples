# Project 46: Queue Watchdog — Alerting When a WordPress Publishing Queue Runs Low

gurmezin.com has one rule: there is always at least one scheduled post on the site. This script checks the rule every hour. It reads the scheduled (`status=future`) posts through the WordPress REST API, puts the queue into one of four states and sends a desktop notification for anything but TAMAM. State names and messages are in Turkish.

| State | When? | Exit code |
|-------|-------|-----------|
| TAMAM (ok) | At least two scheduled posts and the next publishing slot (Mon/Thu 10:00) is filled | 0 |
| UYARI (warning) | Only one post left, or the next publishing slot is empty | 1 |
| KRİTİK (critical) | No scheduled posts, or a post more than 30 minutes past its time is still unpublished | 2 |
| HATA (error) | The queue could not be read (network, auth, server) | 3 |

The watchdog was set up on 15.10.2026. Two holes were closed on 19.10.2026:

1. When the server closed the connection without a response (`RemoteDisconnected`), the script crashed: no log line, no notification. The first `except` clause only caught `URLError` and `TimeoutError`. Errors raised after the connection is established arrive unwrapped, as `OSError` or `http.client.HTTPException`.
2. A post WordPress failed to publish on time ("Missed schedule") counted as TAMAM, because the watchdog only looked at upcoming slots.

The `--demo` option shows both holes without a server or credentials.

## Project Structure
```text
46_queue_watchdog/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer (`list[dict]` annotations). Tested with Python 3.12.3 (Ubuntu 24.04) and Docker `python:3.9-slim` (`--network none`, `--demo` only). Python 3.8 fails with `TypeError: 'type' object is not subscriptable`.
- Standard library only.
- For a real check: a WordPress application password and the `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` environment variables. Notifications need `notify-send` (`libnotify-bin` on Ubuntu).
- Publishing days and hour are constants at the top of the code (`YAYIN_GUNLERI`, `YAYIN_SAATI`).

## Run
```bash
python3 main.py --demo    # offline demonstration
python3 main.py           # check once a day (exits silently if today's state is already logged)
python3 main.py --zorla   # check now even if today's state is logged
```

Results are appended as JSON lines to `kuyruk_bekcisi.log` next to `main.py`. `--demo` writes no files.

Cron example (minute 5 of every hour). If the computer is off in the morning, the check runs in the first hour it is on:

```text
5 * * * * /bin/bash -ic 'python3 /path/main.py' 2>&1 >/dev/null | grep -v -e 'no job control' -e 'terminal process group' >> /path/kuyruk_bekcisi.err
```

`bash -ic` is needed when the credentials live in `~/.bashrc`: Ubuntu's `.bashrc` returns early in a non-interactive shell. The `grep -v` filters the warnings an interactive shell without a terminal prints on every run. If an exception escapes, its traceback ends up in the `.err` file.

## Sample Output (`--demo`, Python 3.12.3, Ubuntu 24.04)
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

One line from a real check (`--zorla`, 19.10.2026):

```text
TAMAM: 2 zamanlanmış yazı, en sonuncusu 26.10 10:00.
```

## Limitations
- The site and the computer are assumed to be in the same time zone (the WordPress `date` field is in site time).
- A post stuck within the 30-minute grace period (`GECIKME_PAYI`) does not raise an alarm yet. The grace keeps WP-Cron's usual few-minute delay from causing false alarms.
- A corrupted JSON line in the log makes `bugun_kaydedildi()` raise.

## Resources
- Blog post: https://gurmezin.com/2026/10/29/claude-ile-otomasyon-4-yayin-kuyruguna-bekci-koyduk/
- WordPress REST API, posts: https://developer.wordpress.org/rest-api/reference/posts/
- `http.client` exceptions: https://docs.python.org/3/library/http.client.html#http.client.RemoteDisconnected
- `urllib.error`: https://docs.python.org/3/library/urllib.error.html
