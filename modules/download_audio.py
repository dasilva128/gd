#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Updated by Grok

import yt_dlp
import re
import logging

async def download_audio(url):
    class MyLogger:
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): logging.error(msg)

    def my_hook(d):
        if d['status'] == 'finished':
            logging.info('Done downloading, now converting ...')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = info['title']
            filename = re.sub(r'[\[\](){}<>\-|]', '', filename).strip() + '.mp3'
            ydl_opts['outtmpl'] = filename
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return filename
    except Exception as e:
        logging.error(f"Audio download error: {e}")
        return f"ERROR CODE-2b-2: {str(e)}"