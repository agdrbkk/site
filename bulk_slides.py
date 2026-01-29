import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_slides_bulk():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('slides', 'v1', credentials=creds)
    
    # 1. สร้างสไลด์ใหม่
    presentation = service.presentations().create(body={'title': 'Proposal: Office Renovation (Final Content)'}).execute()
    p_id = presentation.get('presentationId')
    
    slide_data = [
        ("Project Overview", "เป้าหมายหลัก:\n1. Optimizing Function: เปลี่ยนโกดังเก่าให้เป็นออฟฟิศที่ใช้งานได้จริง\n2. Future Growth: วางผังรวมโรงงานให้เป็นระบบเพื่อรองรับอนาคต"),
        ("Scope 1: Office Renovation", "- Site Survey & Analysis\n- Space Planning (Zoning/Circulation)\n- Interior Design (Mood & Tone)\n- M&E Coordination (Lighting/AC)"),
        ("Scope 2: Factory Masterplan", "- Zoning Analysis ทั่วโครงการ\n- Logistics & Flow Planning (รถขนส่ง/สินค้า)\n- Expansion Planning (ตำแหน่งอาคารในอนาคต)\n- Landscaping & Utilities System"),
        ("Design Process", "Step 1: Conceptual Design (Mood & Tone)\nStep 2: Schematic Design (Layout & 3D)\nStep 3: Masterplan Development\nStep 4: Final Presentation & Preliminary Budget"),
        ("Professional Fee & Contact", "1. งานส่วน Renovation: [ระบุราคา]\n2. งานส่วน Masterplan: [ระบุราคา]\nติดต่อ: [เบอร์โทร/Line แจ็ค]")
    ]

    requests = []
    # หน้าปก
    title_id = presentation.get('slides')[0].get('pageElements')[0]['objectId']
    subtitle_id = presentation.get('slides')[0].get('pageElements')[1]['objectId']
    requests.append({'insertText': {'objectId': title_id, 'text': 'Proposal: Office Renovation & Masterplan'}})
    requests.append({'insertText': {'objectId': subtitle_id, 'text': 'ลูกค้า: คุณส้ม & คุณนนท์\nจัดทำโดย: แจ็ค\nวันที่: 28 มกราคม 2026'}})

    # สร้างสไลด์หน้าอื่นๆ พร้อมระบุ ID ล่วงหน้าเพื่อให้ใส่ข้อความได้ทันที
    for i, (title, body) in enumerate(slide_data):
        slide_id = f"slide_{i}"
        title_id = f"title_{i}"
        body_id = f"body_{i}"
        
        # สร้างสไลด์และระบุ ID ของ placeholder
        requests.append({
            'createSlide': {
                'objectId': slide_id,
                'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'},
                'placeholderIdMappings': [
                    {'layoutPlaceholder': {'type': 'TITLE'}, 'objectId': title_id},
                    {'layoutPlaceholder': {'type': 'BODY'}, 'objectId': body_id}
                ]
            }
        })
        # ใส่ข้อความ
        requests.append({'insertText': {'objectId': title_id, 'text': title}})
        requests.append({'insertText': {'objectId': body_id, 'text': body}})

    # ส่งคำสั่งทั้งหมดในทีเดียว
    service.presentations().batchUpdate(presentationId=p_id, body={'requests': requests}).execute()
    print(f"URL: https://docs.google.com/presentation/d/{p_id}/edit")

if __name__ == '__main__':
    create_slides_bulk()
