# Import libraries
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from pytube import YouTube
import os, re

# Base variables
DOWNLOAD_LOCATION = "./temp/"

# Send welcome message to new users
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to my youtube downloader bot.')


# Download video from youtube and send to user
def download(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user['id']
    # Check if user message is a valid youtube video link
    link = update.message.text
    pattern = r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
    result = re.match(pattern, link)
    if result:
        # Download video from youtube
        youtube = YouTube(link)
        youtube_stream = youtube.streams.get_highest_resolution()
        youtube_stream.download(DOWNLOAD_LOCATION)
        # Send video to user
        file_name = youtube.streams.get_highest_resolution().default_filename
        file_dir = f"{DOWNLOAD_LOCATION}{file_name}"
        context.bot.send_video(chat_id=user_id, video=open(file_dir, 'rb'), supports_streaming=True)
        # Delete video from disk after sending to user
        os.remove(file_dir)
    else:
        update.message.reply_text('Your link is not valid.')


if __name__ == '__main__':
    updater = Updater(token='TOKEN',
                      request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download))

    updater.start_polling()
    updater.idle()
