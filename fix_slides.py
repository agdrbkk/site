import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_slides():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('slides', 'v1', credentials=creds)
    presentation_id = '1qbGwR0h9ORn1opTh6N03doFDrSGnWYncXM5pVre0Ads'

    # เนื้อหาที่จะใส่
    slide_contents = [
        ("Project Overview", "เป้าหมายหลัก:\n1. Optimizing Function: เปลี่ยนโกดังเก่าให้เป็นออฟฟิศที่ใช้งานได้จริง\n2. Future Growth: วางผังรวมโรงงานให้เป็นระบบเพื่อรองรับอนาคต"),
        ("Scope 1: Office Renovation", "- Site Survey & Analysis\n- Space Planning (Zoning/Circulation)\n- Interior Design (Mood & Tone)\n- M&E Coordination (Lighting/AC)"),
        ("Scope 2: Factory Masterplan", "- Zoning Analysis ทั่วโครงการ\n- Logistics & Flow Planning (รถขนส่ง/สินค้า)\n- Expansion Planning (ตำแหน่งอาคารในอนาคต)\n- Landscaping & Utilities System"),
        ("Design Process", "Step 1: Conceptual Design (Mood & Tone)\nStep 2: Schematic Design (Layout & 3D)\nStep 3: Masterplan Development\nStep 4: Final Presentation & Preliminary Budget")
    ]

    requests = []
    
    # ดึงข้อมูลสไลด์มาเพื่อหา Object ID
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    
    # 1. จัดการหน้าแรก (Cover)
    page_elements = slides[0].get('pageElements', [])
    for element in page_elements:
        if 'shape' in element and element['shape']['shapeType'] == 'TEXT_BOX':
            # ลองหยอดข้อความลงในกล่องข้อความที่มีอยู่
            requests.append({
                'insertText': {
                    'objectId': element['objectId'],
                    'text': 'Proposal: Office Renovation & Masterplan (คุณส้มคุณนนท์)'
                }
            })

    # 2. เพิ่มสไลด์ใหม่พร้อมเนื้อหา
    for title, body in slide_contents:
        # สร้างสไลด์ใหม่แบบ Title and Body
        req_create = {
            'createSlide': {
                'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
            }
        }
        res = service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': [req_create]}).execute()
        new_slide_id = res.get('replies')[0].get('createSlide').get('objectId')
        
        # ดึงรายละเอียดสไลด์ใหม่มาหา ID ของ Title และ Body
        new_presentation = service.presentations().get(presentationId=presentation_id).execute()
        for s in new_presentation.get('slides'):
            if s['objectId'] == new_slide_id:
                for el in s.get('pageElements'):
                    if el.get('placeholder', {}).get('type') == 'TITLE':
                        requests.append({'insertText': {'objectId': el['objectId'], 'text': title}})
                    elif el.get('placeholder', {}).get('type') == 'BODY':
                        requests.append({'insertText': {'objectId': el['objectId'], 'text': body}})

    # รันการอัปเดตทั้งหมด
    service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': requests}).execute()
    print("SUCCESS: Slides updated with content!")

if __name__ == '__main__':
    update_slides()
