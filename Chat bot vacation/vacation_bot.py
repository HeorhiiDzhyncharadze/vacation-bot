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
