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

    # 2. กรองหางานที่เสร็จแล้ว (Done, เสร็จแล้ว, done, DONE)
    completed_tasks = []
    for i, row in enumerate(rows):
        if len(row) > 3 and str(row[3]).lower() == "done": # เปลี่ยนเป็นตัวเล็กให้หมดกันพลาด
            completed_tasks.append((i + 1, row))  # เก็บ index แถวไว้ด้วย

    if not completed_tasks:
        print("ไม่พบงานที่ทำเสร็จแล้วใน Sheet เลยครับ")
        return

    # เตรียมคำสั่งลบแถว
    delete_requests = []
    for row_index, task_data in completed_tasks:
         delete_requests.append({"deleteDimension": {"range": {"sheetId": 0, "dimension": "ROWS", "startIndex": row_index-1, "endIndex": row_index}}})

    # ส่งคำสั่ง Batch Update (ลบแถว)
    body = {'requests': delete_requests}
    delete_response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    
    print(f"SUCCESS: ย้ายงาน {len(completed_tasks)} รายการไป Archive และลบออกจาก Sheet หลักแล้วครับ")

if __name__ == '__main__':
    archive_completed_tasks()
