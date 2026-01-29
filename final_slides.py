import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def fix_it_finally():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('slides', 'v1', credentials=creds)
    # สร้างใหม่เพื่อความคลีน
    presentation = service.presentations().create(body={'title': 'Proposal: คุณส้มคุณนนท์ (Final Version)'}).execute()
    p_id = presentation.get('presentationId')
    
    slide_data = [
        ("Proposal: Office Renovation & Masterplan", "ลูกค้า: คุณส้ม & คุณนนท์\nจัดทำโดย: แจ็ค\nวันที่: 28 มกราคม 2026"),
        ("Project Overview", "เป้าหมายหลัก:\n1. Optimizing Function: เปลี่ยนโกดังเก่าให้เป็นออฟฟิศที่ใช้งานได้จริง\n2. Future Growth: วางผังรวมโรงงานให้เป็นระบบเพื่อรองรับอนาคต"),
        ("Scope 1: Office Renovation", "- Site Survey & Analysis\n- Space Planning (Zoning/Circulation)\n- Interior Design (Mood & Tone)\n- M&E Coordination (Lighting/AC)"),
        ("Scope 2: Factory Masterplan", "- Zoning Analysis ทั่วโครงการ\n- Logistics & Flow Planning (รถขนส่ง/สินค้า)\n- Expansion Planning (ตำแหน่งอาคารในอนาคต)\n- Landscaping & Utilities System"),
        ("Design Process", "Step 1: Conceptual Design (Mood & Tone)\nStep 2: Schematic Design (Layout & 3D)\nStep 3: Masterplan Development\nStep 4: Final Presentation & Preliminary Budget"),
        ("Professional Fee & Contact", "1. งานส่วน Renovation: [ระบุราคา]\n2. งานส่วน Masterplan: [ระบุราคา]\nติดต่อ: [เบอร์โทร/Line แจ็ค]")
    ]

    for title, body in slide_data:
        # 1. สร้างสไลด์
        res = service.presentations().batchUpdate(presentationId=p_id, body={
            'requests': [{'createSlide': {'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}}}]
        }).execute()
        s_id = res.get('replies')[0].get('createSlide').get('objectId')
        
        # 2. ดึงข้อมูลสไลด์มาหา ID ของ Title/Body
        s_info = service.presentations().pages().get(presentationId=p_id, pageObjectId=s_id).execute()
        t_id = ""
        b_id = ""
        for el in s_info.get('pageElements', []):
            pt = el.get('placeholder', {}).get('type')
            if pt == 'TITLE' or pt == 'CENTERED_TITLE': t_id = el['objectId']
            if pt == 'BODY': b_id = el['objectId']
        
        # 3. หยอดข้อความ
        reqs = []
        if t_id: reqs.append({'insertText': {'objectId': t_id, 'text': title}})
        if b_id: reqs.append({'insertText': {'objectId': b_id, 'text': body}})
        if reqs: service.presentations().batchUpdate(presentationId=p_id, body={'requests': reqs}).execute()

    print(f"URL: https://docs.google.com/presentation/d/{p_id}/edit")

if __name__ == '__main__':
    fix_it_finally()
