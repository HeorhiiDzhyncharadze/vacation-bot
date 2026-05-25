# Vacation Bot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the vacation Telegram bot with SQLite persistence, 3-language support (UK/EN/HU), hardcoded 12h shift, days-based "used" input, and smart repeat flow.

**Architecture:** Extract pure calculation logic to `calc.py`, async SQLite CRUD to `db.py`, all localised strings to `strings.py`, and rewrite handlers in `vacation_bot.py`. Each module has one responsibility and is independently testable.

**Tech Stack:** Python 3.11+, python-telegram-bot ≥ 21 (async), aiosqlite, pytest, pytest-asyncio

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `calc.py` | Create | Pure calculation + report formatting |
| `db.py` | Create | Async SQLite CRUD |
| `strings.py` | Create | All localised strings + month names |
| `vacation_bot.py` | Rewrite | Telegram handlers only |
| `requirements.txt` | Update | Add aiosqlite |
| `requirements-dev.txt` | Create | pytest, pytest-asyncio |
| `tests/test_calc.py` | Create | Unit tests for calc.py |
| `tests/test_db.py` | Create | Async unit tests for db.py |
| `.gitignore` | Create | Exclude users.db, __pycache__ |

---

## Task 1: Create strings.py

**Files:**
- Create: `strings.py`

- [ ] **Step 1: Write strings.py**

```python
MONTHS = {
    'uk': ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
           "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"],
    'en': ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"],
    'hu': ["Január", "Február", "Március", "Április", "Május", "Június",
           "Július", "Augusztus", "Szeptember", "Október", "November", "December"],
}

STRINGS = {
    'uk': {
        'choose_lang': '🇺🇦 Оберіть мову / 🇬🇧 Choose language / 🇭🇺 Válasszon nyelvet:',
        'welcome': 'Привіт! Порахую доступну відпустку по місяцях.\n\n/calc — розрахунок\n/reset — очистити дані\n/cancel — скасувати',
        'ask_total': 'Скільки *годин відпустки* за рік? (напр. 168)',
        'ask_start_default': 'Початок відпусткового року — *Січень*. Змінити?',
        'btn_yes': 'Так', 'btn_no': 'Ні',
        'ask_end': 'Місяць *закінчення* контракту:',
        'ask_used': 'Скільки *днів* вже використано?',
        'saved_prompt': 'Збережено: *{total}* год, {start}–{end}.\nСкільки *днів* вже використано?',
        'reset_done': 'Параметри видалено. /calc запитає все заново.',
        'reset_none': 'Немає збережених даних.',
        'cancelled': 'Скасовано. /calc щоб почати знову.',
        'err_positive': 'Введи число більше 0 (напр. 168).',
        'err_nonneg': 'Введи 0 або більше (напр. 6).',
        'report_header': '📊 *Розрахунок відпустки*',
        'contract_line': 'Контракт: {start} – {end} ({dur} міс.)',
        'total_line': 'Усього: {total_h:.0f} год = {total_d:.1f} дн  |  Залишок: *{rem_d:.1f} дн*',
        'col_month': 'Місяць', 'col_accrued': 'Накоп', 'col_avail': 'Дост.',
        'disclaimer': '_Орієнтовно, не юридична консультація._',
        'calc_again': 'Ще раз — /calc',
    },
    'en': {
        'choose_lang': '🇺🇦 Оберіть мову / 🇬🇧 Choose language / 🇭🇺 Válasszon nyelvet:',
        'welcome': 'Hi! I will calculate your available vacation by month.\n\n/calc — calculate\n/reset — clear data\n/cancel — cancel',
        'ask_total': 'How many *vacation hours* per year? (e.g. 168)',
        'ask_start_default': 'Vacation year starts *January*. Change?',
        'btn_yes': 'Yes', 'btn_no': 'No',
        'ask_end': '*End* month of contract:',
        'ask_used': 'How many *days* already used?',
        'saved_prompt': 'Saved: *{total}* h, {start}–{end}.\nHow many *days* already used?',
        'reset_done': 'Data cleared. /calc will ask everything again.',
        'reset_none': 'No saved data.',
        'cancelled': 'Cancelled. /calc to start again.',
        'err_positive': 'Enter a number greater than 0 (e.g. 168).',
        'err_nonneg': 'Enter 0 or more (e.g. 6).',
        'report_header': '📊 *Vacation Report*',
        'contract_line': 'Contract: {start} – {end} ({dur} months)',
        'total_line': 'Total: {total_h:.0f} h = {total_d:.1f} d  |  Remaining: *{rem_d:.1f} d*',
        'col_month': 'Month', 'col_accrued': 'Accr.', 'col_avail': 'Avail.',
        'disclaimer': '_Approximate, not legal advice._',
        'calc_again': 'Again — /calc',
    },
    'hu': {
        'choose_lang': '🇺🇦 Оберіть мову / 🇬🇧 Choose language / 🇭🇺 Válasszon nyelvet:',
        'welcome': 'Szia! Kiszámolom az elérhető szabadnapjaidat havonta.\n\n/calc — számítás\n/reset — adatok törlése\n/cancel — mégse',
        'ask_total': 'Hány *szabadságóra* jár évente? (pl. 168)',
        'ask_start_default': 'A szabadságév kezdete *Január*. Megváltoztatja?',
        'btn_yes': 'Igen', 'btn_no': 'Nem',
        'ask_end': 'A szerződés *vége* melyik hónapban?',
        'ask_used': 'Hány *napot* vett már ki?',
        'saved_prompt': 'Mentve: *{total}* óra, {start}–{end}.\nHány *napot* vett már ki?',
        'reset_done': 'Adatok törölve. A /calc mindent újra kérdez.',
        'reset_none': 'Nincs mentett adat.',
        'cancelled': 'Megszakítva. /calc az újrakezdéshez.',
        'err_positive': 'Adjon meg 0-nál nagyobb számot (pl. 168).',
        'err_nonneg': 'Adjon meg 0-t vagy annál nagyobb számot (pl. 6).',
        'report_header': '📊 *Szabadság kalkulátor*',
        'contract_line': 'Szerződés: {start} – {end} ({dur} hó)',
        'total_line': 'Összesen: {total_h:.0f} óra = {total_d:.1f} nap  |  Maradék: *{rem_d:.1f} nap*',
        'col_month': 'Hónap', 'col_accrued': 'Felhalm.', 'col_avail': 'Elérh.',
        'disclaimer': '_Tájékoztató jellegű, nem jogi tanácsadás._',
        'calc_again': 'Újra — /calc',
    },
}
```

- [ ] **Step 2: Commit**

```bash
git add strings.py
git commit -m "feat: add i18n strings (UK/EN/HU)"
```

---

## Task 2: Create calc.py with TDD

**Files:**
- Create: `calc.py`
- Create: `tests/__init__.py` (empty)
- Create: `tests/test_calc.py`

- [ ] **Step 1: Write failing tests**

Create `tests/__init__.py` (empty file), then `tests/test_calc.py`:

```python
import pytest
from calc import build_report, parse_positive, parse_nonneg, SHIFT


def test_shift_is_12():
    assert SHIFT == 12.0


def test_parse_positive_valid():
    assert parse_positive("168") == 168.0
    assert parse_positive("168,5") == 168.5
    assert parse_positive("  12.0 ") == 12.0


def test_parse_positive_rejects_zero():
    with pytest.raises(ValueError):
        parse_positive("0")


def test_parse_positive_rejects_negative():
    with pytest.raises(ValueError):
        parse_positive("-5")


def test_parse_positive_rejects_text():
    with pytest.raises(ValueError):
        parse_positive("abc")


def test_parse_nonneg_zero_ok():
    assert parse_nonneg("0") == 0.0


def test_parse_nonneg_positive_ok():
    assert parse_nonneg("6") == 6.0


def test_parse_nonneg_rejects_negative():
    with pytest.raises(ValueError):
        parse_nonneg("-1")


def test_reference_case_may():
    # total=168h, used=6d(72h), Jan-Oct; May n=5: accrued=84h, avail=12h=1.0d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = [l for l in report.split('\n') if 'Травень' in l]
    assert lines, "May line missing"
    assert '1.0' in lines[0], f"Expected 1.0 in May line, got: {lines[0]}"


def test_reference_case_june():
    # June n=6: accrued=100.8h, avail=28.8h=2.4d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = [l for l in report.split('\n') if 'Червень' in l]
    assert lines, "June line missing"
    assert '2.4' in lines[0], f"Expected 2.4 in June line, got: {lines[0]}"


def test_reference_case_october():
    # October n=10: accrued=168h, avail=96h=8.0d
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = [l for l in report.split('\n') if 'Жовтень' in l]
    assert lines, "October line missing"
    assert '8.0' in lines[0], f"Expected 8.0 in October line, got: {lines[0]}"


def test_clamp_zero_first_months():
    # January: accrued=16.8h, used=72h → avail=0 (clamped)
    report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang='uk')
    lines = [l for l in report.split('\n') if 'Січень' in l]
    assert lines, "January line missing"
    # strip arrow (present when test runs in January), then check last number
    line_clean = lines[0].replace(' ←', '').strip()
    parts = line_clean.split()
    assert parts[-1] == '0.0', f"Expected 0.0, got: {parts[-1]}"


def test_cross_year_duration():
    # Nov(11) to Mar(3): (3-11)%12+1 = 5 months
    report = build_report(total=120, used_days=0, start_m=11, end_m=3, lang='uk')
    assert '5' in report


def test_cross_year_wraps_months():
    # Should contain Листопад, Грудень, Січень, Лютий, Березень
    report = build_report(total=120, used_days=0, start_m=11, end_m=3, lang='uk')
    for month in ['Листопад', 'Грудень', 'Січень', 'Лютий', 'Березень']:
        assert month in report, f"{month} missing in cross-year report"


def test_zero_used():
    report = build_report(total=120, used_days=0, start_m=1, end_m=10, lang='uk')
    # First month: accrued=12h=1.0d, avail=1.0d
    lines = [l for l in report.split('\n') if 'Січень' in l]
    assert lines
    line_clean = lines[0].replace(' ←', '').strip()
    parts = line_clean.split()
    assert parts[-1] == '1.0'


def test_all_languages_produce_output():
    for lang in ['uk', 'en', 'hu']:
        report = build_report(total=168, used_days=6, start_m=1, end_m=10, lang=lang)
        assert len(report) > 100, f"Report for lang={lang} too short"


def test_english_month_names():
    report = build_report(total=168, used_days=6, start_m=1, end_m=3, lang='en')
    assert 'January' in report
    assert 'February' in report
    assert 'March' in report


def test_hungarian_month_names():
    report = build_report(total=168, used_days=6, start_m=1, end_m=3, lang='hu')
    assert 'Január' in report
```

- [ ] **Step 2: Run tests — expect failure**

```
pytest tests/test_calc.py -v
```

Expected: `ModuleNotFoundError: No module named 'calc'`

- [ ] **Step 3: Write calc.py**

```python
import datetime
from strings import STRINGS, MONTHS

SHIFT = 12.0


def parse_positive(text: str) -> float:
    val = float(text.replace(",", ".").strip())
    if val <= 0:
        raise ValueError
    return val


def parse_nonneg(text: str) -> float:
    val = float(text.replace(",", ".").strip())
    if val < 0:
        raise ValueError
    return val


def build_report(total: float, used_days: float, start_m: int, end_m: int, lang: str) -> str:
    s = STRINGS[lang]
    months = MONTHS[lang]
    used_h = used_days * SHIFT
    duration = (end_m - start_m) % 12 + 1
    rate = total / duration
    rem_h = max(0.0, total - used_h)
    rem_d = rem_h / SHIFT
    total_d = total / SHIFT
    current_month = datetime.date.today().month

    lines = [
        s['report_header'],
        "",
        s['contract_line'].format(start=months[start_m - 1], end=months[end_m - 1], dur=duration),
        s['total_line'].format(total_h=total, total_d=total_d, rem_d=rem_d),
        "",
        "```",
        f"{s['col_month']:<11}{s['col_accrued']:>8}{s['col_avail']:>8}",
        "─" * 27,
    ]

    for n in range(1, duration + 1):
        cal = (start_m - 1 + (n - 1)) % 12 + 1
        accrued_h = rate * n
        avail_h = max(0.0, accrued_h - used_h)
        accrued_d = accrued_h / SHIFT
        avail_d = avail_h / SHIFT
        arrow = " ←" if cal == current_month else ""
        lines.append(f"{months[cal - 1]:<11}{accrued_d:>8.1f}{avail_d:>8.1f}{arrow}")

    lines.append("```")
    lines.append("")
    lines.append(s['disclaimer'])

    return "\n".join(lines)
```

- [ ] **Step 4: Run tests — expect all pass**

```
pytest tests/test_calc.py -v
```

Expected: all green

- [ ] **Step 5: Commit**

```bash
git add calc.py tests/__init__.py tests/test_calc.py
git commit -m "feat: add calc.py with full test coverage"
```

---

## Task 3: Create db.py with TDD

**Files:**
- Create: `db.py`
- Create: `tests/test_db.py`
- Create: `requirements-dev.txt`

- [ ] **Step 1: Create requirements-dev.txt**

```
pytest>=7
pytest-asyncio>=0.21
```

Install: `pip install -r requirements-dev.txt`

- [ ] **Step 2: Write failing db tests**

Create `tests/test_db.py`:

```python
import pytest
import db


@pytest.fixture(autouse=True)
def use_tmp_db(monkeypatch, tmp_path):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))


@pytest.mark.asyncio
async def test_init_db_creates_table():
    await db.init_db()
    # no exception = table created


@pytest.mark.asyncio
async def test_get_nonexistent_user_returns_none():
    await db.init_db()
    result = await db.get_user(999)
    assert result is None


@pytest.mark.asyncio
async def test_save_and_get_user():
    await db.init_db()
    await db.save_user(123, 168.0, 1, 10, 'uk')
    user = await db.get_user(123)
    assert user is not None
    assert user["total"] == 168.0
    assert user["start_m"] == 1
    assert user["end_m"] == 10
    assert user["lang"] == 'uk'


@pytest.mark.asyncio
async def test_save_user_replaces_existing():
    await db.init_db()
    await db.save_user(123, 168.0, 1, 10, 'uk')
    await db.save_user(123, 200.0, 2, 11, 'en')
    user = await db.get_user(123)
    assert user["total"] == 200.0
    assert user["lang"] == 'en'


@pytest.mark.asyncio
async def test_delete_user():
    await db.init_db()
    await db.save_user(123, 168.0, 1, 10, 'uk')
    await db.delete_user(123)
    user = await db.get_user(123)
    assert user is None


@pytest.mark.asyncio
async def test_delete_nonexistent_user_is_safe():
    await db.init_db()
    await db.delete_user(999)  # should not raise


@pytest.mark.asyncio
async def test_update_lang():
    await db.init_db()
    await db.save_user(123, 168.0, 1, 10, 'uk')
    await db.update_lang(123, 'hu')
    user = await db.get_user(123)
    assert user["lang"] == 'hu'


@pytest.mark.asyncio
async def test_multiple_users_isolated():
    await db.init_db()
    await db.save_user(1, 168.0, 1, 10, 'uk')
    await db.save_user(2, 240.0, 3, 12, 'en')
    u1 = await db.get_user(1)
    u2 = await db.get_user(2)
    assert u1["total"] == 168.0
    assert u2["total"] == 240.0
```

- [ ] **Step 3: Run tests — expect failure**

```
pytest tests/test_db.py -v
```

Expected: `ModuleNotFoundError: No module named 'db'`

- [ ] **Step 4: Write db.py**

```python
import os
import aiosqlite

DB_PATH = os.environ.get("DB_PATH", "users.db")

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id  INTEGER PRIMARY KEY,
    total    REAL    NOT NULL,
    start_m  INTEGER NOT NULL DEFAULT 1,
    end_m    INTEGER NOT NULL,
    lang     TEXT    NOT NULL DEFAULT 'uk'
)
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(_CREATE_TABLE)
        await conn.commit()


async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def save_user(user_id: int, total: float, start_m: int, end_m: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT OR REPLACE INTO users (user_id, total, start_m, end_m, lang) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, total, start_m, end_m, lang),
        )
        await conn.commit()


async def delete_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await conn.commit()


async def update_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id)
        )
        await conn.commit()
```

- [ ] **Step 5: Add pytest-asyncio config**

Add `pytest.ini` (or section to existing config):

```ini
[pytest]
asyncio_mode = auto
```

- [ ] **Step 6: Run tests — expect all pass**

```
pytest tests/test_db.py -v
```

Expected: all green

- [ ] **Step 7: Commit**

```bash
git add db.py tests/test_db.py requirements-dev.txt pytest.ini
git commit -m "feat: add db.py with SQLite persistence and tests"
```

---

## Task 4: Rewrite vacation_bot.py

**Files:**
- Modify: `vacation_bot.py` (full rewrite)
- Update: `requirements.txt`
- Create: `.gitignore`

- [ ] **Step 1: Update requirements.txt**

```
python-telegram-bot>=21
aiosqlite
```

- [ ] **Step 2: Create .gitignore**

```
users.db
*.db
__pycache__/
*.pyc
.env
```

- [ ] **Step 3: Rewrite vacation_bot.py**

```python
import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import db
from calc import build_report, parse_nonneg, parse_positive
from strings import MONTHS, STRINGS

TOKEN = os.environ["BOT_TOKEN"]

TOTAL, CHANGE_START, START_M, END_M, USED = range(5)

logging.basicConfig(level=logging.INFO)


def t(lang: str, key: str) -> str:
    return STRINGS[lang][key]


def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "uk")


def month_keyboard(prefix: str, lang: str) -> InlineKeyboardMarkup:
    months = MONTHS[lang]
    rows, row = [], []
    for i, name in enumerate(months, 1):
        row.append(InlineKeyboardButton(name, callback_data=f"{prefix}{i}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇭🇺 Magyar", callback_data="lang_hu"),
    ]])
    await update.message.reply_text(
        "🇺🇦 Оберіть мову / 🇬🇧 Choose language / 🇭🇺 Válasszon nyelvet:",
        reply_markup=keyboard,
    )


async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = q.data.replace("lang_", "")
    context.user_data["lang"] = lang
    user_id = q.from_user.id
    if await db.get_user(user_id):
        await db.update_lang(user_id, lang)
    await q.edit_message_text(t(lang, "welcome"))


async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    saved = await db.get_user(user_id)
    if saved:
        lang = saved["lang"]
        context.user_data.update(
            lang=lang,
            total=saved["total"],
            start_m=saved["start_m"],
            end_m=saved["end_m"],
        )
        months = MONTHS[lang]
        prompt = t(lang, "saved_prompt").format(
            total=saved["total"],
            start=months[saved["start_m"] - 1],
            end=months[saved["end_m"] - 1],
        )
        await update.message.reply_text(prompt, parse_mode="Markdown")
        return USED

    lang = get_lang(context)
    await update.message.reply_text(t(lang, "ask_total"), parse_mode="Markdown")
    return TOTAL


async def got_total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    try:
        context.user_data["total"] = parse_positive(update.message.text)
    except ValueError:
        await update.message.reply_text(t(lang, "err_positive"))
        return TOTAL
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_no"), callback_data="cs_no"),
        InlineKeyboardButton(t(lang, "btn_yes"), callback_data="cs_yes"),
    ]])
    await update.message.reply_text(
        t(lang, "ask_start_default"), parse_mode="Markdown", reply_markup=keyboard
    )
    return CHANGE_START


async def got_change_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    if q.data == "cs_no":
        context.user_data["start_m"] = 1
        await q.edit_message_text(MONTHS[lang][0])
        await q.message.reply_text(
            t(lang, "ask_end"), parse_mode="Markdown", reply_markup=month_keyboard("em_", lang)
        )
        return END_M
    await q.edit_message_text(
        t(lang, "ask_start_default"), parse_mode="Markdown", reply_markup=month_keyboard("sm_", lang)
    )
    return START_M


async def got_start_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    context.user_data["start_m"] = int(q.data.replace("sm_", ""))
    await q.edit_message_text(MONTHS[lang][context.user_data["start_m"] - 1])
    await q.message.reply_text(
        t(lang, "ask_end"), parse_mode="Markdown", reply_markup=month_keyboard("em_", lang)
    )
    return END_M


async def got_end_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    context.user_data["end_m"] = int(q.data.replace("em_", ""))
    await q.edit_message_text(MONTHS[lang][context.user_data["end_m"] - 1])
    await q.message.reply_text(t(lang, "ask_used"), parse_mode="Markdown")
    return USED


async def got_used(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    try:
        used_days = parse_nonneg(update.message.text)
    except ValueError:
        await update.message.reply_text(t(lang, "err_nonneg"))
        return USED
    d = context.user_data
    await db.save_user(update.effective_user.id, d["total"], d["start_m"], d["end_m"], lang)
    report = build_report(d["total"], used_days, d["start_m"], d["end_m"], lang)
    await update.message.reply_text(report, parse_mode="Markdown")
    await update.message.reply_text(t(lang, "calc_again"))
    return ConversationHandler.END


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    user_id = update.effective_user.id
    if await db.get_user(user_id):
        await db.delete_user(user_id)
        await update.message.reply_text(t(lang, "reset_done"))
    else:
        await update.message.reply_text(t(lang, "reset_none"))


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(t(lang, "cancelled"))
    return ConversationHandler.END


async def _on_startup(app: Application):
    await db.init_db()


def main():
    app = Application.builder().token(TOKEN).post_init(_on_startup).build()
    app.add_handler(CallbackQueryHandler(set_lang, pattern="^lang_"))
    conv = ConversationHandler(
        entry_points=[CommandHandler("calc", calc)],
        states={
            TOTAL:        [MessageHandler(filters.TEXT & ~filters.COMMAND, got_total)],
            CHANGE_START: [CallbackQueryHandler(got_change_start, pattern="^cs_")],
            START_M:      [CallbackQueryHandler(got_start_month, pattern="^sm_")],
            END_M:        [CallbackQueryHandler(got_end_month, pattern="^em_")],
            USED:         [MessageHandler(filters.TEXT & ~filters.COMMAND, got_used)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CommandHandler("reset", reset))
    print("Bot running. Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run all tests**

```
pytest tests/ -v
```

Expected: all green

- [ ] **Step 5: Commit**

```bash
git add vacation_bot.py requirements.txt .gitignore
git commit -m "feat: rewrite bot with SQLite persistence and 3-language support"
```

---

## Task 5: Smoke test

**No automated tests for Telegram handlers — manual verification.**

- [ ] **Step 1: Set token and run**

```bash
BOT_TOKEN="your_token_here" python vacation_bot.py
```

- [ ] **Step 2: Verify first-run flow**

In Telegram:
1. `/start` → sees 3 language buttons
2. Tap 🇺🇦 → sees welcome message in Ukrainian
3. `/calc` → asked for total hours
4. Enter `168` → asked "Змінити?" with Так/Ні buttons
5. Tap Ні → asked for end month (keyboard)
6. Select Жовтень → asked for used days
7. Enter `6` → sees report with May=1.0, Jun=2.4, Oct=8.0

- [ ] **Step 3: Verify repeat flow**

8. `/calc` again → sees "Збережено: 168 год, Січень–Жовтень. Скільки днів?"
9. Enter `0` → sees report (all months show full accrual)

- [ ] **Step 4: Verify reset**

10. `/reset` → "Параметри видалено"
11. `/calc` → full flow again (asks total hours)

- [ ] **Step 5: Verify English flow**

12. `/start` → tap 🇬🇧 → welcome in English
13. `/calc` → full flow in English

- [ ] **Step 6: Final commit**

```bash
git add .
git commit -m "feat: vacation bot v2 complete — SQLite, i18n UK/EN/HU, smart repeat flow"
```
