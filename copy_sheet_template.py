import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def find_and_copy_sheet():
    creds = Credentials.from_authorized_user_file('token.json')
    drive_service = build('drive', 'v3', credentials=creds)

    # 1. ค้นหาไฟล์ชื่อ "ประเมินราคา"
    results = drive_service.files().list(
        q="name contains 'ประเมินราคา' and mimeType = 'application/vnd.google-apps.spreadsheet'",
        spaces='drive',
        fields='files(id, name)'
    ).execute()
    items = results.get('files', [])

    if not items:
        print("ERROR: ไม่เจอไฟล์ชื่อ 'ประเมินราคา' ใน Drive เลยครับแจ็ค")
        return

    # เลือกไฟล์ตัวแรกที่เจอ
    source_id = items[0]['id']
    source_name = items[0]['name']
    print(f"FOUND: เจอไฟล์ '{source_name}' (ID: {source_id})")

    # 2. Copy ไฟล์
    new_name = "ประเมินราคา - คุณส้มคุณนนท์ (Office & Masterplan)"
    copy_body = {'name': new_name}
    new_file = drive_service.files().copy(fileId=source_id, body=copy_body).execute()
    new_id = new_file.get('id')

    print(f"SUCCESS: สร้างไฟล์ใหม่แล้วชื่อ '{new_name}'")
    print(f"URL: https://docs.google.com/spreadsheets/d/{new_id}/edit")

if __name__ == '__main__':
    find_and_copy_sheet()
