import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
AUTO_REPLY = "Привет! 👋\n\nЯ сейчас недоступен, но обязательно отвечу тебе, как только смогу. Спасибо за терпение! 🤖"

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.business_message:
        return
    msg = update.business_message
    try:
        await context.bot.send_message(
            chat_id=msg.chat_id,
            text=AUTO_REPLY,
            business_connection_id=msg.business_connection_id,
        )
        logger.info(f"Ответил в чат {msg.chat_id}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
