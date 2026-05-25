# 🏖️ Vacation Calculator Bot

> **Telegram-бот для розрахунку доступних днів відпустки по місяцях.**  
> A Telegram bot that calculates available vacation days month by month.

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-≥21-blue)](https://python-telegram-bot.org)
[![SQLite](https://img.shields.io/badge/SQLite-aiosqlite-lightblue?logo=sqlite)](https://sqlite.org)
[![Languages](https://img.shields.io/badge/Languages-🇺🇦_🇬🇧_🇭🇺-green)](#)
[![Tests](https://img.shields.io/badge/Tests-61%20passing-brightgreen)](#testing)

---

## What it does

Many employees struggle to track how many vacation days they have left each month — especially on fixed-term contracts. This bot calculates available vacation days for each month of a contract, based on **linear annual accrual**: vacation hours are earned uniformly across the calendar year.

**Example:** 168 hours/year, 0 days used, January–October contract:

```
📊 Vacation Report

✅ Right now (May): 5.8 d available to take

Month          Accr.   Avail.
───────────────────────────
January          1.2     1.2
February         2.3     2.3
March            3.5     3.5
April            4.7     4.7
May ←            5.8     5.8
June             7.0     7.0
July             8.2     8.2
August           9.3     9.3
September       10.5    10.5
October         11.7    11.7

Contract: January – October (10 months)
Total: 168 h = 14.0 d  |  Remaining by contract end: 11.7 d
```

---

## Features

- 🔢 **Hungarian Labour Code calculator** — automatic entitlement by age + children count (Act I of 2012, §§ 117–118)
- 📅 **Period or annual hours** — enter total hours for the full year *or* for your contract period; bot converts automatically
- 💼 **Opening balance** — carry over unused (or overused) hours from a previous period
- 🗓️ **Smart accrual** — handles contracts spanning New Year (e.g. November → March)
- ⬅️ **Current month highlighted** with headline + arrow
- 🌍 **3 languages** — 🇺🇦 Ukrainian · 🇬🇧 English · 🇭🇺 Hungarian
- 💾 **Persistent settings** — contract data saved per user; `/calc` only asks for days used on return
- ⏱️ **Auto-cancel** — incomplete flows time out after 5 minutes of inactivity
- ☁️ **Cloud-ready** — token from env var, SQLite for persistence, Railway deployment

---

## Architecture

```
strings.py        # i18n — month names + all UI strings (uk/en/hu)
calc.py           # pure calculation logic, no Telegram dependencies
db.py             # async SQLite CRUD (aiosqlite)
vacation_bot.py   # Telegram ConversationHandler + command handlers
tests/
  test_calc.py    # 49 unit tests — accrual formula, HU law, opening balance, languages
  test_db.py      # 12 async tests — full CRUD + opening_balance column migration
```

Each module has **one responsibility** and is independently testable.

---

## Calculation Logic

```
duration   = (end_month − start_month) % 12 + 1   # works across New Year
rate       = annual_hours / 12                      # monthly accrual (annual basis)
accrued(n) = rate × n                               # after n months into contract
available  = opening_balance + accrued(n) − used_h  # no clamping — deficit shown
days       = hours / shift_hours                    # shift = 12 h/day for display
```

The entitlement is always treated as **annual** (full calendar year). For partial-year contracts, the bot asks whether you know your annual figure or only the prorated amount, and converts accordingly.

---

## Setup

### Requirements

- Python 3.12+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Install

```bash
git clone https://github.com/HeorhiiDzhyncharadze/vacation-bot.git
cd "vacation-bot"
pip install -r requirements.txt
```

### Run locally

```bash
# Windows PowerShell
$env:BOT_TOKEN="your_token_here"
python "vacation bot.py"

# Linux / macOS
BOT_TOKEN="your_token_here" python "vacation bot.py"
```

### Run tests

```bash
python -m pytest tests/ -v
```

---

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Choose language (🇺🇦 🇬🇧 🇭🇺) |
| `/calc` | Run the calculation |
| `/reset` | Clear saved contract data |
| `/cancel` | Cancel current flow |
| `/help` | Show feature overview |

---

## Deploy to Railway

1. Fork / push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
3. Add environment variable: `BOT_TOKEN` = your token
4. Railway auto-deploys on every push — bot runs 24/7

> If Railway doesn't auto-detect the start command, add a `Procfile`:
> ```
> worker: python "vacation bot.py"
> ```

---

## Testing

61 tests, all passing:

```
tests/test_calc.py  (49 tests)
  - Annual accrual formula: rate = total/12
  - Hungarian Labour Code: age + children bonuses, 8h workday
  - Opening balance (positive/negative)
  - Report headline (current month availability)
  - Cross-year contracts (Nov→Mar = 5 months)
  - Input validation (nan/inf/negative/zero rejected)
  - All 3 languages produce correct output

tests/test_db.py    (12 tests)
  - Full CRUD: save, get, replace, delete, update_lang
  - opening_balance column + migration idempotency
  - Multi-user isolation
```

---

## About

Built as a portfolio project while learning Python and transitioning to **data analytics / analytics engineering**.

The bot solves a real problem: calculating vacation availability on fixed-term contracts is error-prone when done manually. This automates it for a small team of shift workers in Ukraine and Hungary.

**Tech stack:** Python 3.12 · python-telegram-bot ≥21 · aiosqlite · SQLite · pytest · pytest-asyncio · Railway

---

*Approximate calculations only. Consult your HR for legally binding figures.*
