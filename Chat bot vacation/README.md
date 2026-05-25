# 🏖️ Vacation Calculator Bot

> **Telegram-бот для розрахунку доступних днів відпустки по місяцях.**
> A Telegram bot that calculates available vacation days month by month.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-≥21-blue)](https://python-telegram-bot.org)
[![SQLite](https://img.shields.io/badge/SQLite-aiosqlite-lightblue?logo=sqlite)](https://sqlite.org)
[![Languages](https://img.shields.io/badge/Languages-🇺🇦_🇬🇧_🇭🇺-green)](#)
[![Tests](https://img.shields.io/badge/Tests-28%20passing-brightgreen)](#testing)

---

## What it does

Many employees struggle to track how many vacation days they have left each month — especially on fixed-term contracts. This bot calculates available vacation days for each month of a contract, based on **linear accrual**: vacation hours are earned uniformly across the contract period.

**Example:** 168 hours total (14 days), 6 days already used, January–October contract:

```
📊 Vacation Report

Contract: January – October (10 months)
Total: 168 h = 14.0 d  |  Remaining: 8.0 d

Month          Accr.   Avail.
───────────────────────────
January          1.4      0.0
February         2.8      0.0
March            4.2      0.0
April            5.6      0.0
May ←            7.0      1.0
June             8.4      2.4
July             9.8      3.8
August          11.2      5.2
September       12.6      6.6
October         14.0      8.0
```

---

## Features

- 🇺🇦 **3 languages** — Ukrainian, English, Hungarian
- 💾 **Remembers your settings** — run `/calc` again and it only asks for days used
- 📅 **Smart accrual** — handles contracts that span New Year (e.g. November → March)
- ⬅️ **Current month highlighted** with an arrow
- 🔄 **`/reset`** to clear saved data and start fresh
- ☁️ **Cloud-ready** — token from env var, SQLite for persistence

---

## Architecture

```
strings.py        # i18n data — month names + all UI strings (UK/EN/HU)
calc.py           # pure calculation logic, no Telegram dependencies
db.py             # async SQLite CRUD (aiosqlite)
vacation_bot.py   # Telegram handlers only
tests/
  test_calc.py    # 20 unit tests — reference case, clamping, cross-year, languages
  test_db.py      # 8 async tests — full CRUD coverage
```

Each module has **one responsibility** and is independently testable.

---

## Calculation logic

```
duration = (end_month - start_month) % 12 + 1   # works across New Year
rate = total_hours / duration                     # hours accrued per month
accrued_h = rate * n                              # after n months
available_h = max(0, accrued_h - used_h)         # clamped to 0
available_days = available_h / 12                 # shift = 12h/day
```

Shift (hours per working day) is hardcoded at **12 hours** — common in Ukraine/Hungary for shift workers.

---

## Setup

### Requirements

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Install

```bash
git clone https://github.com/djincharadze/vacation-bot.git
cd vacation-bot
pip install -r requirements.txt
```

### Run locally

```bash
# Windows PowerShell
$env:BOT_TOKEN="your_token_here"
python vacation_bot.py

# Linux / macOS
BOT_TOKEN="your_token_here" python vacation_bot.py
```

### Run tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

---

## Bot commands

| Command | Description |
|---------|-------------|
| `/start` | Choose language (🇺🇦 🇬🇧 🇭🇺) |
| `/calc` | Calculate vacation (smart: asks only used days if settings saved) |
| `/reset` | Clear saved settings |
| `/cancel` | Cancel current calculation |

---

## Deploy to Railway

1. Fork / push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
3. Add environment variable: `BOT_TOKEN` = your token
4. Railway auto-deploys on every push — bot runs 24/7

No `Procfile` needed — Railway detects `python vacation_bot.py` from the repo root.

> **Note:** Add a `Procfile` if Railway doesn't auto-detect:
> ```
> worker: python vacation_bot.py
> ```

---

## Testing

28 tests, all passing:

```
tests/test_calc.py  (20 tests)
  - Reference case: May=1.0d, Jun=2.4d, Oct=8.0d
  - Clamp to zero for early months
  - Cross-year duration (Nov→Mar = 5 months)
  - All 3 languages produce correct output
  - Input validation (nan/inf/negative/zero rejected)

tests/test_db.py    (8 tests)
  - Full CRUD: save, get, replace, delete, update_lang
  - Multi-user isolation
  - Safe delete of non-existent user
```

---

## About

Built as a portfolio project while learning Python and transitioning to **data analytics / analytics engineering**.

The bot solves a real problem: calculating vacation availability on fixed-term contracts is error-prone when done manually. This automates it for a small team.

**Tech stack:** Python 3.11 · python-telegram-bot ≥21 · aiosqlite · SQLite · pytest · pytest-asyncio

---

*Approximate calculations only. Consult your HR for legally binding figures.*
