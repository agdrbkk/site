import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets'
]

def exchange_code_for_token(code):
    flow = InstalledAppFlow.from_client_secrets_file('google_credentials.json', SCOPES)
    flow.redirect_uri = 'http://localhost'
    flow.fetch_token(code=code)
    
    # บันทึก token ลงไฟล์
    credentials = flow.credentials
    with open('token.json', 'w') as token_file:
        token_file.write(credentials.to_json())
    print("SUCCESS: Full access token created!")

if __name__ == '__main__':
    auth_code = '4/0ASc3gC0dq5yNjDc_D7lkDSyCCvj0ekqHP83VbVeFJrwMNPQBG4rLCSz2I-bKcKUH2KklkA'
    # ผมต้องแก้ตัวแปร credentials ให้ถูกนิดหน่อย
