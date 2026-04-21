import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ENV (Render)
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN or not ADMIN_ID:
    raise Exception("Missing TOKEN or ADMIN_ID in environment variables")

ADMIN_ID = int(ADMIN_ID)

# состояние пользователей
user_state = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🧪 Тест", "💬 Поддержка"]]

    await update.message.reply_text(
        "🌐 SUI Network | Support & Verification\n\nДобро пожаловать!",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# тест
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = "test"
    await update.message.reply_text("Отправьте адрес SUI (0x...)")

# поддержка
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = "support"

    keyboard = [["❌ Завершить диалог"]]

    await update.message.reply_text(
        "💬 Вы вошли в поддержку. Напишите сообщение оператору.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# обработка сообщений
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
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"User {uid}: {text}"
        )
        await update.message.reply_text("📨 Отправлено оператору")
    else:
        await update.message.reply_text("Нажмите /start")

# запуск
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle))

    app.run_polling()

# ВАЖНО: правильный entry point
if name == "__main__":
    main()
