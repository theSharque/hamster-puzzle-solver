import logging
import os
from io import BytesIO
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import converter
import solver

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Access from @{update.effective_user.username}")
    await update.message.reply_text("Привет! Я могу помочь с решением головоломки для Hamster combat. Просто загрузи мне скриншот с головоломкой.")


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    logger.info(f"Puzzle from @{update.effective_user.username}")

    out = BytesIO(
        await photo_file.download_as_bytearray(pool_timeout=30, connect_timeout=30, read_timeout=30, write_timeout=30))
    await update.message.reply_text("Великолепно! Дай мне немного времени, мне нужно подумать...")

    image_rows = converter.translate_to_rows(out)
    result = solver.calc(image_rows)
    await update.message.reply_animation(result, 500, 300, 300, "А вот и решение!")


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    if token is None:
        logger.error("You must provide a token as system environment variable!!!")
        exit(1)

    application = (Application.builder()
                   .token(token)
                   .connect_timeout(30)
                   .get_updates_connect_timeout(30)
                   .get_updates_pool_timeout(30)
                   .build())

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("help", info), MessageHandler(filters.PHOTO, photo)],
        states={},
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=10)


if __name__ == "__main__":
    main()
