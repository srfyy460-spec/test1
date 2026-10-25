import os
import asyncio

from telegram import Update
from telegram.request import HTTPXRequest
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "ربات با موفقیت فعال است."
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 ربات آنلاین است.")


async def main():

    if not TOKEN:
        raise RuntimeError("BOT_TOKEN تنظیم نشده است.")

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60
    )

    app = (
        Application.builder()
        .token(TOKEN)
        .request(request)
        .get_updates_request(request)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    print("در حال اتصال به Telegram...")

    for attempt in range(5):
        try:
            await app.initialize()
            print("✅ اتصال به Telegram برقرار شد.")
            break

        except Exception as e:
            print(f"❌ تلاش {attempt + 1} ناموفق بود: {e}")

            if attempt == 4:
                raise

            await asyncio.sleep(10)

    await app.start()
    await app.updater.start_polling()

    print("🤖 Bot is running...")

    try:
        await asyncio.Event().wait()

    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
