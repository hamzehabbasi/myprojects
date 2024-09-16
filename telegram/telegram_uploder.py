from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات خود را اینجا قرار دهید
TOKEN = '6718051921:AAFiblrJVXtL99WA4BtIC8y62QiQARWbMlc'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('سلام! لطفاً فایل خود را برای آپلود ارسال کنید.')

async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = update.message.document
    if file:
        file_id = file.file_id
        new_file = await context.bot.get_file(file_id)
        await new_file.download_to_drive(f'./{file.file_name}')
        link = f"http://yourserver.com/{file.file_name}"  # تغییر آدرس به آدرس سرور شما
        await update.message.reply_text(f"فایل با موفقیت آپلود شد! لینک دانلود: {link}")
    else:
        await update.message.reply_text("لطفاً یک فایل معتبر ارسال کنید.")

async def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, upload_file))

    await app.run_polling()

# if __name__ == '__main__':
#     import asyncio
#     # asyncio.run(main())
