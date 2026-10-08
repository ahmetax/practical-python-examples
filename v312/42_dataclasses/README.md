# Project 42: Python Dataclasses Tour

A runnable walkthrough of the `dataclasses` module: how `@dataclass` replaces hand-written boilerplate and which options are worth knowing. A three-field class that takes 13 lines written by hand shrinks to 5 lines as a dataclass.

| # | Topic | Key API |
|---|-------|---------|
| 1 | Auto-generated `__init__`, `__repr__`, `__eq__` | `@dataclass` |
| 2 | Default values and the mutable default trap | `field(default_factory=list)` |
| 3 | Validation and computed fields | `__post_init__`, `field(init=False)` |
| 4 | Immutable, hashable value objects | `frozen=True`, `replace()` |
| 5 | Sorting instances by field order | `order=True`, `field(compare=False)` |
| 6 | Keyword-only arguments and lighter objects (with a memory benchmark) | `kw_only=True`, `slots=True` |
| 7 | Converting nested dataclasses to JSON | `asdict()` |

## Project Structure
```text
42_dataclasses/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer (`slots` and `kw_only` were added in 3.10). Tested on 3.12.3.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
== 5. order=True ==
['3.9.0', '3.10.14', '3.12.3', '3.15.0']
max          : Version(major=3, minor=15, patch=0, label='rc')

== 6. kw_only ve slots ==
hata         : UserSlots.__init__() takes 1 positional argument but 4 were given
hata         : 'UserSlots' object has no attribute 'nickname'
100.000 nesne (normal):   19,806 KB
100.000 nesne (slots) :   16,678 KB  (%16 daha az)
```
Output labels are in Turkish to match the accompanying blog post. Memory figures depend on the machine and Python version. The measurement includes the name and email strings, so the saving per object is about 32 bytes.

## Further Reading
- Blog post (Turkish): https://gurmezin.com/2026/10/08/pythonda-dataclasses-sinif-yazmanin-kisa-yolu/
- `dataclasses` documentation: https://docs.python.org/3/library/dataclasses.html
- PEP 557: Data Classes
