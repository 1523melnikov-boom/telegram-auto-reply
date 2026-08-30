import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Тексты ответов
AUTO_REPLY = "Привет! 👋\n\nЯ сейчас недоступен, но обязательно отвечу тебе, как только смогу. Спасибо за терпение! 🤖"
HOW_ARE_YOU_REPLY = "У меня всё отлично, спасибо! А у тебя как дела? 😊"

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


async def how_are_you(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /howareyou"""
    await update.message.reply_text(HOW_ARE_YOU_REPLY)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    text = update.message.text.lower()

    # Если спрашивают "как дела"
    if "как дела" in text or "как ты" in text or "как поживаешь" in text:
        await update.message.reply_text(HOW_ARE_YOU_REPLY)
        return

    # Обычный автоответ
    await update.message.reply_text(AUTO_REPLY)


async def business_auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Автоответ через Business Connection (Secretary Mode)"""
    if not update.business_message:
        return
    msg = update.business_message
    text = msg.text.lower() if msg.text else ""

    try:
        # Если спрашивают "как дела" в бизнес-чате
        if "как дела" in text or "как ты" in text or "как поживаешь" in text:
            await context.bot.send_message(
                chat_id=msg.chat_id,
                text=HOW_ARE_YOU_REPLY,
                business_connection_id=msg.business_connection_id,
            )
        else:
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

    # Команда /howareyou
    app.add_handler(CommandHandler("howareyou", how_are_you))

    # Обычные сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    # Business messages (Secretary Mode)
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, business_auto_reply))

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
