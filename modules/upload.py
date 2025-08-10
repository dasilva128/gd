#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Updated by Grok

import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from mimetypes import guess_type
from modules.credentials import Creds

async def upload_to_drive(filename):
    logging.basicConfig(level="ERROR")
    token_file = os.path.join(os.path.dirname(__file__), 'auth_token.json')

    try:
        if not os.path.exists(token_file):
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": Creds.CLIENT_ID,
                    "client_secret": Creds.CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
                }
            }, scopes=['https://www.googleapis.com/auth/drive.file'])
            creds = flow.run_console()
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        else:
            creds = Credentials.from_authorized_user_file(token_file)

        drive_service = build('drive', 'v3', credentials=creds)
        mime_type = guess_type(filename)[0] or 'text/plain'
        file_name = os.path.basename(filename)

        file_metadata = {
            'name': file_name,
            'description': 'backup',
            'mimeType': mime_type
        }
        media = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()

        permission = {'type': 'anyone', 'role': 'reader'}
        drive_service.permissions().create(fileId=file['id'], body=permission).execute()

        return file.get('webViewLink')
    except Exception as e:
        logging.error(f"Upload error: {e}")
        return f"ERROR: {str(e)}"