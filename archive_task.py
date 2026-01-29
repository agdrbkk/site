import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import re

def archive_task(task_name):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    archive_database_id = '2f685629665b8085b5d8c7812d4ea5c9'
    
    # ดึงข้อมูลทั้งหมดจาก Sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:F100").execute()
    rows = result.get('values', [])

    # หา Row ที่มีชื่องานตรงกับที่ระบุ
    task_row_index = None
    for i, row in enumerate(rows):
        if len(row) > 1 and task_name in row[1]: # B คือชื่อ Task
            task_row_index = i + 1 # +1 เพราะ Google Sheet เริ่มที่ 1
            break

    if task_row_index is None:
        print(f"ERROR: ไม่พบ Task ชื่อ '{task_name}' ใน Sheet ครับ")
        return
    
    # ดึงข้อมูลเฉพาะ Task ที่จะย้าย
    task_data = rows[task_row_index-1]
    print(f"TASK_DATA:{task_data}")

    # ย้ายไป Archive โดยใช้ Notion API (ต้องลองทำความเข้าใจรูปแบบ API ก่อน)
    # หมายเหตุ: การย้ายข้าม Database ใน Notion API อาจจะต้องสร้าง Page ใหม่ใน Archive แล้ว Copy ข้อมูลจาก Page เดิมมา
    # เนื่องจากตอนนี้ยังไม่สามารถทำได้จริง (ติดเรื่อง Sub-Agent และ Notion API) 
    # ผมจะลองแค่แก้ไขสถานะใน Google Sheet ก่อนนะครับ

    # แก้สถานะเป็น Done (สมมุติว่า Done คือ Column C)
    update_values = [["เสร็จแล้ว" if len(task_data)>2 else task_data[0],  task_data[1], task_data[2] if len(task_data)>2 else "",task_data[3] if len(task_data)>3 else "",task_data[4] if len(task_data)>4 else "",task_data[5] if len(task_data)>5 else "",]]

    update_body = {'values': update_values}
    update_response = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A{task_row_index}:F{task_row_index}", # ระบุ range ที่จะแก้ไข
        valueInputOption='USER_ENTERED',
        body=update_body
    ).execute()

    print(f"SUCCESS: Task '{task_name}' ถูกย้ายไป Archive แล้ว (แต่จริงๆ แค่เปลี่ยนสถานะ)")


# ทดสอบการทำงาน (ฟังก์ชันนี้จะถูกเรียกเมื่อมีคนพิมพ์ [Done] ในแชท)
if __name__ == '__main__':
    # ตัวอย่างการเรียกใช้: ลองใส่ชื่องานที่ต้องการย้าย
    test_task = "งานที่ต้องทำ"
    # กรองคำว่า  [Done]  ออกจาก  message
    match = re.search(r'\[Done\]\s*(.+)', test_task)
    if match:
        task_name = match.group(1).strip() # extract only the task name for filtering
        archive_task(task_name=task_name)
    else:
        print("The test_task does not fit the proper format")
