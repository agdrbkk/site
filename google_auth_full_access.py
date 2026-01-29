import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# เปลี่ยน Scope เป็นแบบจัดเต็ม (เข้าถึง Drive ทั้งหมด)
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_auth_url():
    flow = InstalledAppFlow.from_client_secrets_file('google_credentials.json', SCOPES)
    flow.redirect_uri = 'http://localhost'
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    print(f"URL: {auth_url}")

if __name__ == '__main__':
    get_auth_url()
