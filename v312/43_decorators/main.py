# Author: Ahmet Aksoy
# Date: 08.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.9+

"""
Python Decorators Tour
A hands-on walkthrough of decorators: functions as objects and closures,
a timing decorator, why functools.wraps matters, decorators with arguments
(retry), functools.cache on Fibonacci (with call counts and timings),
a command registry and the order of stacked decorators.
"""
import functools
import time


# --- 1. Fonksiyonlar da nesnedir: closure -------------------------------------
def make_multiplier(factor):
    def multiply(x):
        return x * factor          # factor, dış fonksiyondan "hatırlanıyor"
    return multiply


def demo_closure():
    print("== 1. Fonksiyonlar nesnedir ==")
    double, triple = make_multiplier(2), make_multiplier(3)
    print("double(21)   :", double(21))
    print("triple(21)   :", triple(21))
    print("double nedir :", double.__qualname__)


# --- 2. İlk dekoratör: süre ölçmek ---------------------------------------------
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"[timer] {func.__name__} {elapsed:.1f} ms sürdü")
        return result
    return wrapper


@timer
def slow_sum(n):
    return sum(i * i for i in range(n))


def demo_timer():
    print("\n== 2. @timer ==")
    print("sonuç        :", slow_sum(1_000_000))


# --- 3. functools.wraps neden gerekli? ------------------------------------------
def without_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def with_wraps(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@without_wraps
def greet_a(name):
    """Kullanıcıyı selamlar."""
    return f"Merhaba {name}"


@with_wraps
def greet_b(name):
    """Kullanıcıyı selamlar."""
    return f"Merhaba {name}"


def demo_wraps():
    print("\n== 3. functools.wraps ==")
    print(f"wraps yok    : {greet_a.__name__!r}, doc={greet_a.__doc__!r}")
    print(f"wraps var    : {greet_b.__name__!r}, doc={greet_b.__doc__!r}")


# --- 4. Parametre alan dekoratör: retry -----------------------------------------
def retry(times=3, exceptions=(Exception,), delay=0.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    print(f"[retry] {func.__name__} deneme {attempt}/{times} başarısız: {exc}")
                    if attempt == times:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


calls = {"count": 0}


@retry(times=3, exceptions=(ConnectionError,))
def fetch_rates():
    calls["count"] += 1
    if calls["count"] < 3:                      # ilk iki çağrı başarısız olsun
        raise ConnectionError("sunucu yanıt vermedi")
    return {"USD": 41.6, "EUR": 48.4}


@retry(times=2, exceptions=(ConnectionError,))
def parse_price(text):
    return float(text)


def demo_retry():
    print("\n== 4. @retry(times=3) ==")
    print("sonuç        :", fetch_rates())
    try:
        parse_price("kırk iki")
    except ValueError as exc:
        print("ValueError yeniden denenmedi:", exc)


# --- 5. Hazır dekoratör: functools.cache --------------------------------------
fib_calls = 0


def fib(n):
    global fib_calls
    fib_calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)


cached_calls = 0


@functools.cache
def fib_cached(n):
    global cached_calls
    cached_calls += 1
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)


def demo_cache():
    print("\n== 5. @functools.cache ==")
    start = time.perf_counter()
    result = fib(30)
    plain_ms = (time.perf_counter() - start) * 1000
    start = time.perf_counter()
    cached = fib_cached(30)
    cached_ms = (time.perf_counter() - start) * 1000
    print(f"fib(30) önbelleksiz: {result}, {fib_calls:>9,} çağrı, {plain_ms:8.1f} ms")
    print(f"fib(30) önbellekli : {cached}, {cached_calls:>9,} çağrı, {cached_ms:8.3f} ms")
    print("cache_info   :", fib_cached.cache_info())


# --- 6. Kayıt (registry) dekoratörü: komut tablosu ---------------------------
COMMANDS = {}


def command(name):
    def decorator(func):
        COMMANDS[name] = func       # fonksiyonu değiştirmeden kaydeder
        return func
    return decorator


@command("selam")
def cmd_hello(arg):
    return f"Selam, {arg}!"


@command("ters")
def cmd_reverse(arg):
    return arg[::-1]


def demo_registry():
    print("\n== 6. Kayıt dekoratörü ==")
    print("komutlar     :", sorted(COMMANDS))
    for line in ["selam Ayşe", "ters gurmezin", "sil dosya"]:
        name, _, arg = line.partition(" ")
        handler = COMMANDS.get(name)
        print(f"{line:<14}->", handler(arg) if handler else f"bilinmeyen komut: {name}")


# --- 7. Üst üste dekoratörler: sıra önemli -----------------------------------
def bold(func):
    @functools.wraps(func)
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper


def italic(func):
    @functools.wraps(func)
    def wrapper():
        return f"<i>{func()}</i>"
    return wrapper


@bold
@italic
def title_a():
    return "gurmezin"


@italic
@bold
def title_b():
    return "gurmezin"


def demo_stacking():
    print("\n== 7. Dekoratör sırası ==")
    print("@bold @italic:", title_a())
    print("@italic @bold:", title_b())


if __name__ == "__main__":
    demo_closure()
    demo_timer()
    demo_wraps()
    demo_retry()
    demo_cache()
    demo_registry()
    demo_stacking()
