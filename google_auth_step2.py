import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
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
    print("SUCCESS: token.json created!")

if __name__ == '__main__':
    # ใส่ code ที่แจ็คส่งมา
    auth_code = '4/0ASc3gC2mCjY1WsslIumRITN_5aNQrzotXU3J6EOReLGPzVEvqh-M3cLWUhGHtf3sgtZn1g'
    exchange_code_for_token(auth_code)
