import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
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
from calc import (
    build_report,
    parse_finite,
    parse_nonneg,
    parse_nonneg_int,
    parse_positive,
    vacation_days_hu,
    vacation_hours_hu,
)
from strings import MONTHS, STRINGS

TOKEN = os.environ["BOT_TOKEN"]

KNOW_HOURS, TOTAL, AGE, CHILDREN, HU_CONFIRM, CHANGE_START, START_M, END_YEAR_YN, END_M, BALANCE_YN, BALANCE_VAL, USED, HOURS_TYPE = range(13)

logging.basicConfig(level=logging.INFO)

_LANG_KEYBOARD = InlineKeyboardMarkup([[
    InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
    InlineKeyboardButton("🇬🇧 English",    callback_data="lang_en"),
    InlineKeyboardButton("🇭🇺 Magyar",     callback_data="lang_hu"),
]])
_LANG_PROMPT = "🇺🇦 Оберіть мову / 🇬🇧 Choose language / 🇭🇺 Válasszon nyelvet:"


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
    await update.message.reply_text(_LANG_PROMPT, reply_markup=_LANG_KEYBOARD)


async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    # Block language change while a /calc conversation is active
    if context.user_data.get("_in_calc"):
        await q.answer("Finish /calc first, then change language. / Спочатку завершіть /calc.")
        return
    await q.answer()
    lang = q.data.replace("lang_", "")
    context.user_data["lang"] = lang
    user_id = q.from_user.id
    if await db.get_user(user_id):
        await db.update_lang(user_id, lang)
    await q.edit_message_text(t(lang, "welcome"))


async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["_in_calc"] = True
    user_id = update.effective_user.id
    saved = await db.get_user(user_id)
    if saved:
        lang = saved["lang"]
        ob = saved.get("opening_balance", 0.0)
        context.user_data.update(
            lang=lang,
            total=saved["total"],
            start_m=saved["start_m"],
            end_m=saved["end_m"],
            opening_balance=ob,
        )
        months = MONTHS[lang]
        prompt = t(lang, "saved_prompt").format(
            total=saved["total"],
            start=months[saved["start_m"] - 1],
            end=months[saved["end_m"] - 1],
            bal=ob,
        )
        await update.message.reply_text(prompt, parse_mode="Markdown")
        return USED

    lang = get_lang(context)
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_kh_yes"),  callback_data="kh_yes"),
        InlineKeyboardButton(t(lang, "btn_kh_calc"), callback_data="kh_calc"),
    ]])
    await update.message.reply_text(
        t(lang, "ask_know_hours"), parse_mode="Markdown", reply_markup=keyboard
    )
    return KNOW_HOURS


async def got_know_hours(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    if q.data == "kh_yes":
        await q.edit_message_text(t(lang, "btn_kh_yes"))
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(t(lang, "btn_cs_keep"),   callback_data="cs_no"),
            InlineKeyboardButton(t(lang, "btn_cs_change"), callback_data="cs_yes"),
        ]])
        await q.message.reply_text(t(lang, "ask_start_default"), parse_mode="Markdown", reply_markup=keyboard)
        return CHANGE_START
    # kh_calc
    await q.edit_message_text(t(lang, "btn_kh_calc"))
    await q.message.reply_text(t(lang, "ask_age"), parse_mode="Markdown")
    return AGE


async def got_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    try:
        age = parse_nonneg_int(update.message.text)
    except (ValueError, TypeError):
        await update.message.reply_text(t(lang, "err_age"))
        return AGE
    context.user_data["_age"] = age
    await update.message.reply_text(t(lang, "ask_children"), parse_mode="Markdown")
    return CHILDREN


async def got_children(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    try:
        children = parse_nonneg_int(update.message.text)
    except (ValueError, TypeError):
        await update.message.reply_text(t(lang, "err_children"))
        return CHILDREN
    age = context.user_data.get("_age", 0)
    days = vacation_days_hu(age, children)
    hours = vacation_hours_hu(age, children)
    context.user_data["total"] = hours
    # Show calculation result
    await update.message.reply_text(
        t(lang, "calc_hu_result").format(age=age, children=children, days=days, hours=hours),
        parse_mode="Markdown",
    )
    # Ask user to confirm calculated hours or enter their own
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_huc_use").format(hours=hours),    callback_data="huc_use"),
        InlineKeyboardButton(t(lang, "btn_huc_change"),                     callback_data="huc_change"),
    ]])
    await update.message.reply_text(
        t(lang, "ask_hu_confirm").format(hours=hours), parse_mode="Markdown", reply_markup=keyboard
    )
    return HU_CONFIRM


async def got_hu_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    hours = context.user_data["total"]
    if q.data == "huc_use":
        await q.edit_message_text(t(lang, "btn_huc_use").format(hours=hours))
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(t(lang, "btn_cs_keep"),   callback_data="cs_no"),
            InlineKeyboardButton(t(lang, "btn_cs_change"), callback_data="cs_yes"),
        ]])
        await q.message.reply_text(
            t(lang, "ask_start_default"), parse_mode="Markdown", reply_markup=keyboard
        )
        return CHANGE_START
    # huc_change: let user enter their own hours (months already collected above)
    context.user_data.pop("total", None)
    await q.edit_message_text(t(lang, "btn_huc_change"))
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_cs_keep"),   callback_data="cs_no"),
        InlineKeyboardButton(t(lang, "btn_cs_change"), callback_data="cs_yes"),
    ]])
    await q.message.reply_text(t(lang, "ask_start_default"), parse_mode="Markdown", reply_markup=keyboard)
    return CHANGE_START


async def _after_end_month(message, context, lang: str) -> int:
    """Decide next state after end_m is stored. Returns the next state constant."""
    start_m  = context.user_data["start_m"]
    end_m    = context.user_data["end_m"]
    duration = (end_m - start_m) % 12 + 1
    months   = MONTHS[lang]

    if "total" in context.user_data:
        # HU path: hours already set → go straight to balance question
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(t(lang, "btn_bal_yes"), callback_data="bal_yes"),
            InlineKeyboardButton(t(lang, "btn_bal_no"),  callback_data="bal_no"),
        ]])
        await message.reply_text(t(lang, "ask_balance_yn"), parse_mode="Markdown", reply_markup=keyboard)
        return BALANCE_YN

    if duration == 12:
        # Full-year contract: period hours = annual hours, no conversion needed
        await message.reply_text(t(lang, "ask_total"), parse_mode="Markdown")
        return TOTAL

    # Partial-year: ask whether user knows period hours or annual hours
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            t(lang, "btn_ht_period").format(
                start=months[start_m - 1], end=months[end_m - 1], dur=duration),
            callback_data="ht_period",
        ),
        InlineKeyboardButton(t(lang, "btn_ht_annual"), callback_data="ht_annual"),
    ]])
    await message.reply_text(
        t(lang, "ask_hours_type").format(
            start=months[start_m - 1], end=months[end_m - 1], dur=duration),
        parse_mode="Markdown", reply_markup=keyboard,
    )
    return HOURS_TYPE


async def got_hours_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    if q.data == "ht_period":
        context.user_data["_period_entry"] = True
        await q.edit_message_text(t(lang, "btn_ht_period_chosen"))
    else:
        await q.edit_message_text(t(lang, "btn_ht_annual"))
    await q.message.reply_text(t(lang, "ask_total"), parse_mode="Markdown")
    return TOTAL


async def got_total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    try:
        hours = parse_positive(update.message.text)
    except ValueError:
        await update.message.reply_text(t(lang, "err_positive"))
        return TOTAL
    if context.user_data.pop("_period_entry", False):
        start_m  = context.user_data["start_m"]
        end_m    = context.user_data["end_m"]
        duration = (end_m - start_m) % 12 + 1
        hours    = round(hours * 12 / duration, 2)
    context.user_data["total"] = hours
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_bal_yes"), callback_data="bal_yes"),
        InlineKeyboardButton(t(lang, "btn_bal_no"),  callback_data="bal_no"),
    ]])
    await update.message.reply_text(t(lang, "ask_balance_yn"), parse_mode="Markdown", reply_markup=keyboard)
    return BALANCE_YN


async def got_change_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    if q.data == "cs_no":
        context.user_data["start_m"] = 1
        await q.edit_message_text(MONTHS[lang][0])
        end_year_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton(t(lang, "btn_ey_yes"), callback_data="ey_yes"),
            InlineKeyboardButton(t(lang, "btn_ey_no"),  callback_data="ey_no"),
        ]])
        await q.message.reply_text(
            t(lang, "ask_end_year_yn"), parse_mode="Markdown", reply_markup=end_year_kb
        )
        return END_YEAR_YN
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
    end_year_kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_ey_yes"), callback_data="ey_yes"),
        InlineKeyboardButton(t(lang, "btn_ey_no"),  callback_data="ey_no"),
    ]])
    await q.message.reply_text(
        t(lang, "ask_end_year_yn"), parse_mode="Markdown", reply_markup=end_year_kb
    )
    return END_YEAR_YN


async def got_end_year_yn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    if q.data == "ey_yes":
        context.user_data["end_m"] = 12
        await q.edit_message_text(MONTHS[lang][11])  # Грудень / December / December
        return await _after_end_month(q.message, context, lang)
    # ey_no: dismiss buttons, show month picker
    await q.edit_message_text(t(lang, "ask_end_year_yn"), parse_mode="Markdown")
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
    return await _after_end_month(q.message, context, lang)


async def got_balance_yn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = get_lang(context)
    if q.data == "bal_no":
        context.user_data["opening_balance"] = 0.0
        await q.edit_message_text(t(lang, "btn_bal_no"))
        await q.message.reply_text(t(lang, "ask_used"), parse_mode="Markdown")
        return USED
    # bal_yes
    await q.edit_message_text(t(lang, "btn_bal_yes"))
    await q.message.reply_text(t(lang, "ask_balance_val"), parse_mode="Markdown")
    return BALANCE_VAL


async def got_balance_val(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    try:
        val = parse_finite(update.message.text)
    except (ValueError, TypeError):
        await update.message.reply_text(t(lang, "err_balance"))
        return BALANCE_VAL
    context.user_data["opening_balance"] = val
    await update.message.reply_text(t(lang, "ask_used"), parse_mode="Markdown")
    return USED


async def got_used(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    try:
        used_days = parse_nonneg(update.message.text)
    except ValueError:
        await update.message.reply_text(t(lang, "err_nonneg"))
        return USED
    d = context.user_data
    if not all(k in d for k in ("total", "start_m", "end_m")):
        await update.message.reply_text(t(lang, "cancelled"))
        return ConversationHandler.END
    ob = d.get("opening_balance", 0.0)
    await db.save_user(update.effective_user.id, d["total"], d["start_m"], d["end_m"], lang, ob)
    report = build_report(d["total"], used_days, d["start_m"], d["end_m"], lang, opening_balance_h=ob)
    await update.message.reply_text(report, parse_mode="Markdown")
    await update.message.reply_text(t(lang, "calc_again"))
    context.user_data.pop("_in_calc", None)
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
    context.user_data.pop("_in_calc", None)
    await update.message.reply_text(t(lang, "cancelled"))
    await update.message.reply_text(_LANG_PROMPT, reply_markup=_LANG_KEYBOARD)
    return ConversationHandler.END


async def _on_startup(app: Application):
    await db.init_db()

    cmds = {
        'uk': [
            BotCommand("start",  "🌐 Вибір мови"),
            BotCommand("calc",   "🔢 Розрахувати відпустку"),
            BotCommand("reset",  "🗑️ Скинути дані"),
            BotCommand("cancel", "⛔ Скасувати"),
        ],
        'en': [
            BotCommand("start",  "🌐 Choose language"),
            BotCommand("calc",   "🔢 Calculate vacation"),
            BotCommand("reset",  "🗑️ Reset data"),
            BotCommand("cancel", "⛔ Cancel"),
        ],
        'hu': [
            BotCommand("start",  "🌐 Nyelv választás"),
            BotCommand("calc",   "🔢 Szabadság kalkuláció"),
            BotCommand("reset",  "🗑️ Adatok törlése"),
            BotCommand("cancel", "⛔ Megszakítás"),
        ],
    }
    for lang_code, commands in cmds.items():
        await app.bot.set_my_commands(commands, language_code=lang_code)
    await app.bot.set_my_commands(cmds['en'])  # default fallback


def main():
    app = Application.builder().token(TOKEN).post_init(_on_startup).build()
    app.add_handler(CallbackQueryHandler(set_lang, pattern="^lang_"))
    conv = ConversationHandler(
        entry_points=[CommandHandler("calc", calc)],
        states={
            KNOW_HOURS:  [CallbackQueryHandler(got_know_hours, pattern="^kh_")],
            TOTAL:       [MessageHandler(filters.TEXT & ~filters.COMMAND, got_total)],
            AGE:         [MessageHandler(filters.TEXT & ~filters.COMMAND, got_age)],
            CHILDREN:    [MessageHandler(filters.TEXT & ~filters.COMMAND, got_children)],
            HU_CONFIRM:  [CallbackQueryHandler(got_hu_confirm, pattern="^huc_")],
            CHANGE_START:[CallbackQueryHandler(got_change_start, pattern="^cs_")],
            START_M:     [CallbackQueryHandler(got_start_month, pattern="^sm_")],
            END_YEAR_YN: [CallbackQueryHandler(got_end_year_yn, pattern="^ey_")],
            END_M:       [CallbackQueryHandler(got_end_month, pattern="^em_")],
            HOURS_TYPE:  [CallbackQueryHandler(got_hours_type, pattern="^ht_")],
            BALANCE_YN:  [CallbackQueryHandler(got_balance_yn, pattern="^bal_")],
            BALANCE_VAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_balance_val)],
            USED:        [MessageHandler(filters.TEXT & ~filters.COMMAND, got_used)],
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
