import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def archive_completed_tasks():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    archive_database_id = '2f685629665b8085b5d8c7812d4ea5c9'

    # 1. อ่านข้อมูลทั้งหมดจาก Sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:F100").execute()
    rows = result.get('values', [])

    # 2. กรองหางานที่เสร็จแล้ว (สมมติว่า "Done", "เสร็จแล้ว" คือสถานะที่แปลว่าเสร็จ)
    completed_tasks = []
    for i, row in enumerate(rows):
        if len(row) > 3 and (row[3] == "Done" or row[3] == "เสร็จแล้ว"):
            completed_tasks.append((i + 1, row))  # เก็บ index แถวไว้ด้วย

    if not completed_tasks:
        print("ไม่พบงานที่ทำเสร็จแล้วใน Sheet เลยครับ")
        return

    # 3. (ในโลกแห่งความจริง) ย้ายไป Archive (Notion API)\n    # แต่ตอนนี้ทำได้แค่เปลี่ยนสถานะใน Google Sheet เพราะข้อจำกัดด้าน API
    requests = []
    for row_index, task_data in completed_tasks:
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': row_index - 1,  # -1 เพราะ index เริ่มที่ 0
                    'endRowIndex': row_index,
                    'startColumnIndex': 3,
                    'endColumnIndex': 4  # Column D = สถานะ
                },
                'rows': [{
                    'values': [{'userEnteredValue': {'stringValue': 'Archived'}}]  # เปลี่ยนเป็น Archived แทน Done
                }],
                'fields': 'userEnteredValue'
            }
        })

    body = {'requests': requests}
    response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

    print(f"SUCCESS: เปลี่ยนสถานะงาน {len(completed_tasks)} รายการเป็น Archived แล้วครับ")


if __name__ == '__main__':
    archive_completed_tasks()
