#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Updated by Grok

import yt_dlp
import re
import logging

async def download_video(url):
    class MyLogger:
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): logging.error(msg)

    def my_hook(d):
        if d['status'] == 'finished':
            logging.info('Done downloading')

    try:
        with yt_dlp.YoutubeDL({'logger': MyLogger()}) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = re.sub(r'[\[\](){}<>\-|]', '', info['title']).strip() + f".{info['ext']}"
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best' if 'youtube' in url.lower() else 'best',
                'outtmpl': filename,
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return filename
    except Exception as e:
        logging.error(f"Video download error: {e}")
        return f"ERROR CODE-2b-1: {str(e)}"