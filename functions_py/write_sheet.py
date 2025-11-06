# ===============================================
# Rulita, 06-11-2025
# New program for replace program write-sheet.php
# ===============================================

from google.oauth2 import service_account
from googleapiclient.discovery import build
from functions.additional_functions import *

import os
import subprocess
import shutil
import time
import csv
import re
import sys

def write_sheet(file_path:string, link:string):

    def generate_output():
        nonlocal file_path, it_exists
        return {"it_exists": it_exists}
    
    try:
        SERVICE_ACCOUNT_FILE = '/usr1/serverless/src/additional_files/service-account.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        RANGE_NAME = 'macro'
        SPREADSHEET_URL = trim(link) if link else None
        TXT_FILE_PATH = trim(file_path) if file_path != "" else None

        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', SPREADSHEET_URL)
        spreadsheet_id = match.group(1)

        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        service = build('sheets', 'v4', credentials=creds)

        with open(TXT_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(';')
                if len(parts) < 3:
                    continue

                row, col, value = parts
                row = int(row)
                col = int(col)

                if value.strip() == "":
                    continue

                col_letter = chr(ord('A') + col - 1)
                cell_ref = f"{col_letter}{row}"

                service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=f"{RANGE_NAME}!{cell_ref}",
                    valueInputOption='USER_ENTERED',
                    body={'values': [[value]]}
                ).execute()

    except Exception as e:
        print(f"An error occurred: {e}")

    it_exists = True

    return generate_output()