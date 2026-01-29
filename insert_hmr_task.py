import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def insert_hmr_task():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5,Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # ดึงข้อมูลเดิมมาเพื่อเลื่อนแถวลง
    # เราจะแทรกที่ Row 6 (ต่อจาก 1.1)
    # แต่ละรายการมี 1 แถว ดังนั้นเราต้องเลื่อน 1.2 (เดิม) ลงไปเป็น 1.3
    
    # วิธีที่ชัวร์ที่สุดคือดึงข้อมูลทั้งหมดมาจัดใหม่แล้วเขียนทับ
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:F100").execute()
    rows = result.get('values', [])
    
    # สร้าง list ใหม่
    new_rows = []
    for i, row in enumerate(rows):
        if i == 5: # หลังจาก 1.1 (Row 5 ใน Sheet คือ index 4, แต่เราอยากแทรกต่อจาก 1.1)
            # เพิ่ม 1.2 ใหม่
            new_rows.append(["1.2", "งานกั้นผนังเบาพร้อมกรุไม้ HMR และคิ้วตกแต่ง (หักกระจกออก)", "ตร.ม.", "16", "5000", "80000"])
        
        # ขยับลำดับข้อที่เหลือ
        if i >= 5:
            if len(row) > 0 and "." in row[0]:
                parts = row[0].split('.')
                if parts[0] == "1" and int(parts[1]) >= 2:
                    row[0] = f"1.{int(parts[1])+1}"
            new_rows.append(row)
        else:
            new_rows.append(row)

    # เขียนทับทั้งหมด
    body = {'values': new_rows}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A1", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: แทรกรายการ 1.2 (กรุไม้ HMR) เรียบร้อย (16 ตร.ม. @ 5000 บาท)")

if __name__ == '__main__':
    # ผมต้องเช็ค ID อีกทีเผื่อก๊อปมาผิด (ตัว L กับ 1)
    # ID คือ 1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA
    insert_hmr_task()
