import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8669180991:AAGEBejanSR3HeT3yTEpt6upxWgsQTtZbFc
"
ADMIN_ID = 8363290963

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    text = f"📩 Новое сообщение:\n\n👤 @{user.username}\n🆔 {user.id}\n\n💬 {update.message.text}"

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    await update.message.reply_text("✅ Сообщение отправлено в поддержку")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    await app.run_polling()

if name == "__main__":
    asyncio.run(main())
