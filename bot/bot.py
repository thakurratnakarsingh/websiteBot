import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import os

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load the API token from the config file
from config.settings import TELEGRAM_BOT_TOKEN

# Initialize the bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def start(update, context):
    """Send a welcome message."""
    update.message.reply_text('Hello! I am your file upload bot.')

def upload_file(update, context):
    """Upload a file to Telegram."""
    file_path = 'path/to/your/file.txt'
    with open(file_path, 'rb') as f:
        bot.send_document(chat_id=update.message.chat_id, document=f)
    update.message.reply_text('File uploaded!')

def main():
    """Start the bot."""
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handlers for bot commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("upload", upload_file))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
