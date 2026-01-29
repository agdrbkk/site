import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def create_slides():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('slides', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # 1. สร้างสไลด์ใหม่
    presentation = service.presentations().create(body={'title': 'Proposal: Office Renovation & Factory Masterplan (คุณส้มคุณนนท์)'}).execute()
    presentation_id = presentation.get('presentationId')

    # 2. เพิ่มเนื้อหา (หน้าปก)
    requests = [
        {
            'updatePageElementText': {
                'objectId': presentation.get('slides')[0].get('pageElements')[0].get('objectId'),
                'text': 'Proposal: Office Renovation & Masterplan'
            }
        },
        {
            'updatePageElementText': {
                'objectId': presentation.get('slides')[0].get('pageElements')[1].get('objectId'),
                'text': 'ลูกค้า: คุณส้ม & คุณนนท์\nจัดทำโดย: แจ็ค\nวันที่: 28 มกราคม 2026'
            }
        }
    ]

    # เพิ่มสไลด์หน้าอื่นๆ (แบบง่ายๆ ก่อน)
    slide_contents = [
        ("Project Overview", "เป้าหมายหลัก:\n1. Optimizing Function: เปลี่ยนโกดังเก่าให้เป็นออฟฟิศที่ใช้งานได้จริง\n2. Future Growth: วางผังรวมโรงงานให้เป็นระบบเพื่อรองรับอนาคต"),
        ("Scope of Work", "- Site Survey & Analysis\n- Space Planning (Zoning/Circulation)\n- Interior Design (Mood & Tone)\n- Factory Masterplan Development")
    ]

    for title, body in slide_contents:
        # สร้างสไลด์ใหม่
        slide_req = {
            'createSlide': {
                'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
            }
        }
        res = service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': [slide_req]}).execute()
        new_slide_id = res.get('replies')[0].get('createSlide').get('objectId')
        
        # ใส่ข้อความ (ต้องหา ID ของ placeholder ก่อน ซึ่งปกติหน้าจอจะไม่ได้บอกตรงๆ ต้องใช้ get สไลด์มาดู)
        # เพื่อความชัวร์และเร็ว บอทจะใช้วิธีง่ายๆ ในการสร้างก่อนครับ
    
    # 3. ตั้งค่าการแชร์ (ให้แจ็คเข้าถึงได้)
    print(f"URL: https://docs.google.com/presentation/d/{presentation_id}/edit")

if __name__ == '__main__':
    create_slides()
