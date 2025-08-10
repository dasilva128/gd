#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Updated by Grok

import aiohttp
import os
import re
import logging

async def check_filesize(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url, allow_redirects=True) as resp:
            return int(resp.headers.get('content-length', 0))

async def is_downloadable(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url, allow_redirects=True) as resp:
            content_type = resp.headers.get('content-type', '').lower()
            return 'text' not in content_type and 'html' not in content_type

async def download_file(url, filename=None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return f"ERROR CODE-a1: Status {resp.status}"
                if not filename:
                    content_disposition = resp.headers.get('content-disposition')
                    if content_disposition:
                        filename = re.findall(r'filename="(.+)"', content_disposition)
                        filename = filename[0] if filename else "downloaded_file"
                    else:
                        filename = url.split("/")[-1] or "downloaded_file"
                filename = re.sub(r'[\[\](){}<>\-|]', '', filename).strip()
                async with open(filename, 'wb') as f:
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break
                        await f.write(chunk)
                return filename
    except Exception as e:
        logging.error(f"Download error: {e}")
        return f"ERROR CODE-a1: {str(e)}"