import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def format_sheet():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'

    requests = []

    # ตรึง (Freeze) แถว 1-3 และคอลัมน์ A
    requests.append({'updateSheetProperties': {
        'properties': {'gridProperties': {'frozenRowCount': 3, 'frozenColumnCount': 1}},
        'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'
    }})

    # ตีเส้น (Borders) ทั่วทั้งตาราง (สมมติว่ามีข้อมูลไม่เกิน 50 แถว)
    for i in range(1, 51):
        requests.append({'updateBorders': {
            'range': {'sheetId': 0, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 1, 'endColumnIndex': 6},
            'top': {'style': 'SOLID', 'width': 1, 'color': {'red': 0, 'green': 0, 'blue': 0}},
            'bottom': {'style': 'SOLID', 'width': 1, 'color': {'red': 0, 'green': 0, 'blue': 0}},
            'left': {'style': 'SOLID', 'width': 1, 'color': {'red': 0, 'green': 0, 'blue': 0}},
            'right': {'style': 'SOLID', 'width': 1, 'color': {'red': 0, 'green': 0, 'blue': 0}},
            'innerHorizontal': {'style': 'SOLID', 'width': 1, 'color': {'red': 0, 'green': 0, 'blue': 0}},
            'innerVertical': {'style': 'SOLID', 'width': 1, 'color': {'red': 0, 'green': 0, 'blue': 0}}
        }})

    # จัดข้อความกึ่งกลาง
    requests.append({'repeatCell': {
        'range': {'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 50, 'startColumnIndex': 0, 'endColumnIndex': 6},
        'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
        'fields': 'userEnteredFormat.horizontalAlignment'
    }})

    # เน้นสีพื้นหลังหัวข้อ
    for i in range(4, 25, 6): # Row 4, 10, 16, 22,...
        requests.append({'repeatCell': {
            'range': {'sheetId': 0, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
            'cell': {'userEnteredFormat': {'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}}},
            'fields': 'userEnteredFormat.backgroundColor'
        }})

    # สั่งอัปเดต (Batch ทั้งหมด)
    body = {'requests': requests}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

    print("SUCCESS: จัดรูปแบบ Sheet เรียบร้อย")

if __name__ == '__main__':
    format_sheet()
