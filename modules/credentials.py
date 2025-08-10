#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Updated by Grok

import os

class Creds:
    TOKEN = os.getenv("BOT_TOKEN", "your_default_token")
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "your_default_client_id")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "your_default_client_secret")