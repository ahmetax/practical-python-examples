# Project 55: Are the Models Getting Better? The Same Three Tasks, August vs. Today

Projects 31 (merge sort), 32 (binary search tree) and 38 (regex validators) were written by an AI assistant in August and September. Later posts found problems in them that the demo inputs never showed. Here the same three tasks were given again to today's model (Claude Code 2.1.325, `claude-opus-5-5`, tools off, five runs per task). This script checks the old code and one of today's answers with the same 23 tests.

| Area | Old code ("says") | Today's five answers ("model") |
|---|---|---|
| Merge sort: stability, a new list for 0/1 elements | fails 3 tests | all fixed in 5/5 |
| Tree: 1000+ sorted inserts | `RecursionError` | no crash in 5/5 (loops instead of recursion) |
| Tree: duplicate values | kept (`[3, 3, 5, 5, 8]`) | silently dropped in 5/5 (`[3, 5, 8]`) |
| Password check and Turkish letters | `[A-Z]` misses `Ş`, `İ` | fixed in 5/5 |
| Phone: Arabic-Indic digits (`\d`) | accepted | still accepted in 5/5 |
| Phone: trailing newline (`strip()`) | accepted | still accepted in 5/5 |
| Phone: newlines / no-break spaces between groups (`\s?`) | accepted | accepted in 3/5 |
| Email: trailing newline | accepted | accepted in 1/5 (`strip()` before `fullmatch`) |

Of the 13 tests the old code fails, 7 are fixed in all five answers and 6 still fail in at least one answer. The duplicate-values test is new: the old code passes it.

## How It Works
- The three prompts are in `PROMPTS` (the real ones were in Turkish; see the blog post). They do not mention validation, limits or security.
- `SAYS_*` holds the original code from projects 31, 32 and 38 (the functions copied unchanged). `MODEL_*` holds one of today's answers: regex run 4, merge sort run 1, tree run 1. The counts in the table above are over all five runs of each task and come from the blog post.
- Each answer is loaded with `exec` under `__name__ == "answer"`, so its demo block does not run. Output printed by the answer is discarded; exceptions (including `RecursionError`) become the test detail.
- The recursion limit is set to 1000 (the default) so the output is reproducible. The last tree test compares sorted and shuffled insert times, so those two numbers vary between machines.
- To test any other answer: `python3 main.py regex answer.py` (`regex`, `sort` or `tree`).

## Limitations
- The tests come from the problems already found in the old code. Other problems in today's answers can exist; the duplicate-values behaviour was found by reading the answers.
- One model, one prompt per task, five runs each.

## Project Structure
```text
55_model_rerun/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer. Tested on 3.12.3 and in Docker on 3.9 and 3.14; the output was identical apart from the timing numbers.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
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

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/12/03/modeller-iyilesiyor-mu-agustos-projeleri-claude-yeniden-yazdirdik/
- Original projects: `v312/31_custom_sorting_algorithms`, `v312/32_data_structures_bin_tree`, `v312/38_regex_validation`
- Earlier findings: `v312/47_regex_edge_cases`, `v312/51_tested_but_wrong`, `v312/53_lenient_api`
- Python `re` documentation: https://docs.python.org/3/library/re.html
