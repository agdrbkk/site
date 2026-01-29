import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_full_slides():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('slides', 'v1', credentials=creds)
    
    # สร้างไฟล์ใหม่ไปเลยเพื่อความชัวร์ (อันเก่าลบยาก)
    presentation = service.presentations().create(body={'title': 'Proposal: Office Renovation & Factory Masterplan (Final)'}).execute()
    presentation_id = presentation.get('presentationId')

    # หน้าที่ 1: หน้าปก (ใช้ ID เดิมของหน้าแรก)
    slide0 = presentation.get('slides')[0]
    title_id = slide0.get('pageElements')[0]['objectId']
    subtitle_id = slide0.get('pageElements')[1]['objectId']
    
    requests = [
        {'insertText': {'objectId': title_id, 'text': 'Proposal: Office Renovation & Masterplan'}},
        {'insertText': {'objectId': subtitle_id, 'text': 'ลูกค้า: คุณส้ม & คุณนนท์\nจัดทำโดย: แจ็ค\nวันที่: 28 มกราคม 2026'}}
    ]
    service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': requests}).execute()

    # ข้อมูลหน้าอื่นๆ
    slide_data = [
        ("Project Overview", "เป้าหมายหลัก:\n1. Optimizing Function: เปลี่ยนโกดังเก่าให้เป็นออฟฟิศที่ใช้งานได้จริง\n2. Future Growth: วางผังรวมโรงงานให้เป็นระบบเพื่อรองรับอนาคต"),
        ("Scope 1: Office Renovation", "- Site Survey & Analysis\n- Space Planning (Zoning/Circulation)\n- Interior Design (Mood & Tone)\n- M&E Coordination (Lighting/AC)"),
        ("Scope 2: Factory Masterplan", "- Zoning Analysis ทั่วโครงการ\n- Logistics & Flow Planning (รถขนส่ง/สินค้า)\n- Expansion Planning (ตำแหน่งอาคารในอนาคต)\n- Landscaping & Utilities System"),
        ("Design Process", "Step 1: Conceptual Design (Mood & Tone)\nStep 2: Schematic Design (Layout & 3D)\nStep 3: Masterplan Development\nStep 4: Final Presentation & Preliminary Budget"),
        ("Professional Fee & Contact", "1. งานส่วน Renovation: [ระบุราคา]\n2. งานส่วน Masterplan: [ระบุราคา]\nติดต่อ: [เบอร์โทร/Line แจ็ค]")
    ]

    for title, body in slide_data:
        # สร้างสไลด์
        res = service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': [
            {'createSlide': {'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}}}
        ]}).execute()
        new_slide_id = res.get('replies')[0].get('createSlide').get('objectId')
        
        # ดึง ID ของกล่องข้อความในสไลด์ใหม่
        slide_info = service.presentations().pages().get(presentationId=presentation_id, pageObjectId=new_slide_id).execute()
        elements = slide_info.get('pageElements', [])
        
        inner_reqs = []
        for el in elements:
            if el.get('placeholder', {}).get('type') == 'TITLE':
                inner_reqs.append({'insertText': {'objectId': el['objectId'], 'text': title}})
            elif el.get('placeholder', {}).get('type') == 'BODY':
                inner_reqs.append({'insertText': {'objectId': el['objectId'], 'text': body}})
        
        service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': inner_reqs}).execute()

    print(f"URL: https://docs.google.com/presentation/d/{presentation_id}/edit")

if __name__ == '__main__':
    create_full_slides()
