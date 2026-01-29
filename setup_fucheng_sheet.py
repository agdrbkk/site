import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def setup_fucheng_sheet():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # 1. สร้าง Sheet ใหม่
    add_sheet_request = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }]
    }
    try:
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=add_sheet_request).execute()
        print(f"SUCCESS: สร้าง Sheet '{sheet_name}' เรียบร้อยแล้ว")
    except Exception as e:
        print(f"NOTE: Sheet '{sheet_name}' อาจจะมีอยู่แล้ว หรือเกิดข้อผิดพลาด: {e}")

    # 2. เตรียมข้อมูล BOQ
    boq_data = [
        ["รายการประเมินราคา: ร้านข้าวมันไก่ฟู่เฉิง สาขา Go Wholesale รามคำแหง 127", "", ""],
        ["", "", ""],
        ["ลำดับ", "รายการงาน", "หน่วย", "ปริมาณ (ประมาณการ)"],
        ["1", "งานผนังและตกแต่งพื้นผิว", "", ""],
        ["", "- ผนังเบาสมาร์ทบอร์ดปิดผิวลามิเนต (Harmonic Teak)", "ตร.ม.", "45"],
        ["", "- ระแนงไม้ WPC ตกแต่งผนัง (Ocean Conqueror)", "ตร.ม.", "12"],
        ["", "- งานทาสีภายใน (TOA Jasmin)", "ตร.ม.", "60"],
        ["", "- ปูกระเบื้องผนังโซนครัว (30x60 ซม.)", "ตร.ม.", "18"],
        ["", "- คิวตกแต่งไม้ HMR พ่นสีแดง", "เมตร", "25"],
        ["2", "งานพื้น", "", ""],
        ["", "- งานปูกระเบื้องพื้น (60x60 ซม.)", "ตร.ม.", "53"],
        ["3", "งานบิวท์อินและอุปกรณ์", "", ""],
        ["", "- เคาน์เตอร์เขียงและตู้โชว์วัตถุดิบ", "ชุด", "1"],
        ["", "- งานกระจกใสหนา 6 มม. พร้อมโครง", "ตร.ม.", "4"],
        ["", "- กล่องป้ายไฟอะคริลิคหน้าร้าน", "ชุด", "1"],
        ["4", "งานระบบไฟฟ้าและแสงสว่าง", "", ""],
        ["", "- ติดตั้งตู้เมนไฟฟ้า", "ชุด", "1"],
        ["", "- ติดตั้งโคมไฟดาวน์ไลท์", "จุด", "12"],
        ["", "- ติดตั้งชุดรางไฟ Tracklight", "เมตร", "3"],
        ["", "- ติดตั้งไฟเส้น LED Strip Light", "เมตร", "10"],
        ["", "- เดินสายไฟและติดตั้งปลั๊กไฟ", "จุด", "15"],
        ["5", "งานระบบประปาและสุขาภิบาล", "", ""],
        ["", "- ติดตั้งมิเตอร์น้ำและวาล์ว", "ชุด", "1"],
        ["", "- เดินท่อน้ำดี-น้ำเสีย (ซิงค์ล้างจาน)", "จุด", "2"],
        ["6", "งานระบบปรับอากาศและ CCTV", "", ""],
        ["", "- ติดตั้งเครื่องปรับอากาศ (FCU+CDU)", "ชุด", "2"],
        ["", "- ติดตั้งกล้องวงจรปิด CCTV", "จุด", "4"]
    ]

    # 3. หยอดข้อมูลลงใน Sheet ใหม่ (เริ่มที่ A1)
    body = {'values': boq_data}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A1", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: หยอดข้อมูลลงใน Sheet '{sheet_name}' เรียบร้อยแล้ว")
    print(f"URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid=0")

if __name__ == '__main__':
    setup_fucheng_sheet()
