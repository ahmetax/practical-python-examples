# Author: Ahmet Aksoy
# Date: 08.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.10+

"""
Python Dataclasses Tour
A hands-on walkthrough of the dataclasses module: auto-generated __init__,
__repr__ and __eq__, default_factory, __post_init__ validation, frozen
instances with replace(), ordering, slots/kw_only (with a memory benchmark)
and asdict() for JSON export.
"""
import json
import tracemalloc
from dataclasses import FrozenInstanceError, asdict, dataclass, field, replace


# --- 1. Klasik sınıf ile dataclass karşılaştırması -------------------------
class BookClassic:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __repr__(self):
        return f"BookClassic(title={self.title!r}, author={self.author!r}, pages={self.pages!r})"

    def __eq__(self, other):
        if not isinstance(other, BookClassic):
            return NotImplemented
        return (self.title, self.author, self.pages) == (other.title, other.author, other.pages)


@dataclass
class Book:
    title: str
    author: str
    pages: int


def demo_basics():
    print("== 1. Temel kullanım ==")
    a = Book("Tutunamayanlar", "Oğuz Atay", 724)
    b = Book("Tutunamayanlar", "Oğuz Atay", 724)
    print(a)
    print("a == b       :", a == b)
    print("classic repr :", BookClassic("Tutunamayanlar", "Oğuz Atay", 724))


# --- 2. Varsayılan değerler ve değiştirilebilir varsayılan tuzağı ------------
@dataclass
class Shelf:
    name: str
    books: list[Book] = field(default_factory=list)
    capacity: int = 20


def demo_defaults():
    print("\n== 2. Varsayılanlar ve default_factory ==")
    s1, s2 = Shelf("Roman"), Shelf("Bilim")
    s1.books.append(Book("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 382))
    print("s1 kitap sayısı:", len(s1.books))
    print("s2 kitap sayısı:", len(s2.books))
    try:
        @dataclass
        class BadShelf:
            books: list = []
    except ValueError as exc:
        print("hata         :", exc)


# --- 3. __post_init__ ile doğrulama ve türetilmiş alan -----------------------
@dataclass
class Order:
    product: str
    unit_price: float
    quantity: int = 1
    total: float = field(init=False)

    def __post_init__(self):
        if self.quantity < 1:
            raise ValueError(f"quantity must be >= 1, got {self.quantity}")
        self.total = round(self.unit_price * self.quantity, 2)


def demo_post_init():
    print("\n== 3. __post_init__ ==")
    print(Order("Kahve", 145.50, 3))
    try:
        Order("Çay", 40.0, 0)
    except ValueError as exc:
        print("hata         :", exc)


# --- 4. frozen=True: değiştirilemeyen ve hash'lenebilen nesneler -------------
@dataclass(frozen=True)
class Point:
    lat: float
    lon: float


def demo_frozen():
    print("\n== 4. frozen ve replace ==")
    istanbul = Point(41.01, 28.98)
    try:
        istanbul.lat = 0
    except FrozenInstanceError as exc:
        print("hata         :", exc)
    moved = replace(istanbul, lon=29.10)
    print("orijinal     :", istanbul)
    print("replace      :", moved)
    visited = {istanbul: "İstanbul", Point(39.93, 32.86): "Ankara"}
    print("sözlük anahtarı:", visited[Point(41.01, 28.98)])


# --- 5. order=True ile sıralama ------------------------------------------------
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int = 0
    label: str = field(default="", compare=False)


def demo_order():
    print("\n== 5. order=True ==")
    versions = [Version(3, 15, 0, "rc"), Version(3, 9), Version(3, 12, 3), Version(3, 10, 14)]
    print([f"{v.major}.{v.minor}.{v.patch}" for v in sorted(versions)])
    print("max          :", max(versions))


# --- 6. kw_only ve slots ---------------------------------------------------------
@dataclass
class UserPlain:
    name: str
    email: str
    age: int


@dataclass(slots=True, kw_only=True)
class UserSlots:
    name: str
    email: str
    age: int


def memory_kb(cls, n=100_000):
    tracemalloc.start()
    items = [cls(name=f"user{i}", email=f"u{i}@ornek.com", age=i % 90) for i in range(n)]
    size, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del items
    return size / 1024


def demo_slots():
    print("\n== 6. kw_only ve slots ==")
    try:
        UserSlots("Ayşe", "ayse@ornek.com", 31)
    except TypeError as exc:
        print("hata         :", exc)
    u = UserSlots(name="Ayşe", email="ayse@ornek.com", age=31)
    try:
        u.nickname = "ayse31"
    except AttributeError as exc:
        print("hata         :", exc)
    plain, slots = memory_kb(UserPlain), memory_kb(UserSlots)
    print(f"100.000 nesne (normal): {plain:>8,.0f} KB")
    print(f"100.000 nesne (slots) : {slots:>8,.0f} KB  (%{(1 - slots / plain) * 100:.0f} daha az)")


# --- 7. asdict ile JSON'a dönüştürme ------------------------------------------
def demo_asdict():
    print("\n== 7. asdict ve JSON ==")
    shelf = Shelf("Roman", [Book("İnce Memed", "Yaşar Kemal", 436)], capacity=10)
    print(json.dumps(asdict(shelf), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    demo_basics()
    demo_defaults()
    demo_post_init()
    demo_frozen()
    demo_order()
    demo_slots()
    demo_asdict()
