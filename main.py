import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

user_state = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🧪 Тест", "💬 Поддержка"]]

    await update.message.reply_text(
        "🌐 SUI Network | Support & Verification\n\nДобро пожаловать!",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ТЕСТ
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = "test"
    await update.message.reply_text("Отправьте адрес SUI (0x...)")

# ПОДДЕРЖКА
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = "support"
    keyboard = [["❌ Завершить диалог"]]

    await update.message.reply_text(
        "Вы в поддержке. Напишите сообщение.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# сообщения
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if text == "🧪 Тест":
        return await test(update, context)

    if text == "💬 Поддержка":
        return await support(update, context)

    if text == "❌ Завершить диалог":
        user_state[uid] = "main"
        return await start(update, context)

    if user_state.get(uid) == "support":
        await context.bot.send_message(ADMIN_ID, f"User {uid}: {text}")
        await update.message.reply_text("Отправлено в поддержку")
    else:
        await update.message.reply_text("Нажмите /start")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle))

    app.run_polling()

if name == "__main__":
    main()
