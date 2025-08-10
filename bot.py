#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Updated by Grok

import os
import logging
import validators
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, ContextTypes
from modules.download import download_file, is_downloadable, check_filesize
from modules.download_audio import download_audio
from modules.download_video import download_video
from modules.upload import upload_to_drive
from modules.text_data import Text
from modules.credentials import Creds

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(Text.GREET_USER.format(update.message.from_user.first_name))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(Text.HELP, parse_mode="HTML")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("PayPal", url="https://www.paypal.me/AtulKadian")],
        [InlineKeyboardButton("PayTM", url="https://telegra.ph/Like-my-work--Buy-me-some-snacks-01-25")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(Text.DONATE, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    user_id = update.message.from_user.id
    sent_message = await update.message.reply_text(Text.VERIFYING_URL)

    if "|" in msg:
        user_cmd, url = map(str.strip, msg.split("|"))
        user_cmd = user_cmd.lower()
    else:
        user_cmd, url = None, msg

    if not validators.url(url):
        await sent_message.edit_text(Text.RETARD)
        return

    await sent_message.edit_text(Text.PROCESSING)

    try:
        if user_cmd == "video":
            filename = await download_video(url)
            if "ERROR" in filename:
                await sent_message.edit_text(Text.FAILED + filename, parse_mode="HTML")
                return
            await sent_message.edit_text(Text.UPLOADING_GD)
            download_url = await upload_to_drive(filename)
            size = os.path.getsize(filename) / 1048576
            await sent_message.edit_text(Text.DONE.format(filename, size, download_url), parse_mode="HTML")
            os.remove(filename)

        elif user_cmd == "audio":
            if "youtube" in url or "youtu.be" in url:
                filename = await download_audio(url)
                if "ERROR" in filename:
                    await sent_message.edit_text(Text.FAILED + filename, parse_mode="HTML")
                    return
                await sent_message.edit_text(Text.UPLOADING_TG)
                async with context.bot.send_audio(
                    chat_id=update.message.chat_id,
                    audio=open(filename, 'rb'),
                    caption=filename.replace(".mp3", "")
                ):
                    os.remove(filename)
                await sent_message.edit_text(Text.DONE)
            else:
                await sent_message.edit_text(Text.NOT_SUPPORTED, parse_mode="HTML")

        else:
            if is_downloadable(url):
                size = check_filesize(url) / 1048576
                if size <= 10000:
                    filename = await download_file(url, user_cmd)
                    if "ERROR" in filename:
                        await sent_message.edit_text(Text.FAILED + filename, parse_mode="HTML")
                        return
                    await sent_message.edit_text(Text.UPLOADING_GD)
                    download_url = await upload_to_drive(filename)
                    await sent_message.edit_text(Text.DONE.format(filename, size, download_url), parse_mode="HTML")
                    os.remove(filename)
                else:
                    await sent_message.edit_text(Text.MAXLIMITEXCEEDED)
            else:
                await sent_message.edit_text(Text.ISNOT_DOWNLOADABLE, parse_mode="HTML")

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        await sent_message.edit_text(Text.FAILED + f"Error: {str(e)}", parse_mode="HTML")

def main():
    app = Application.builder().token(Creds.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()