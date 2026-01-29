from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_doc_proposal():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('docs', 'v1', credentials=creds)
    
    # 1. สร้างเอกสารใหม่
    doc = service.documents().create(body={'title': 'เนื้อหาสำหรับสไลด์ Proposal - คุณส้มคุณนนท์'}).execute()
    doc_id = doc.get('documentId')
    
    # 2. เตรียมเนื้อหา
    full_text = """PROPOSAL: OFFICE RENOVATION & MASTERPLAN
ลูกค้า: คุณส้ม & คุณนนท์
จัดทำโดย: แจ็ค
วันที่: 28 มกราคม 2026

--------------------------------------------------

หน้า 1: PROJECT OVERVIEW (เป้าหมายหลัก)
1. Optimizing Function: เปลี่ยนโกดังเก่าให้เป็นออฟฟิศที่ใช้งานได้จริง
2. Future Growth: วางผังรวมโรงงานให้เป็นระบบเพื่อรองรับอนาคต

หน้า 2: SCOPE 1 - OFFICE RENOVATION
- Site Survey & Analysis (สำรวจพื้นที่)
- Space Planning (วางผังฟังก์ชัน Zoning/Circulation)
- Interior Design (ออกแบบตกแต่ง Mood & Tone)
- M&E Coordination (งานระบบไฟฟ้า/แสงสว่าง/แอร์)

หน้า 3: SCOPE 2 - FACTORY MASTERPLAN
- Zoning Analysis (วิเคราะห์พื้นที่ทั่วโครงการ)
- Logistics & Flow Planning (ผังจราจรรถขนส่ง/สินค้า)
- Expansion Planning (ตำแหน่งอาคารในอนาคต)
- Landscaping & Utilities System (พื้นที่สีเขียว/งานระบบหลัก)

หน้า 4: DESIGN PROCESS (ขั้นตอนทำงาน)
Step 1: Conceptual Design (สรุป Mood & Tone)
Step 2: Schematic Design (แปลนพื้นอย่างละเอียด & 3D)
Step 3: Masterplan Development (ผังรวมทั้งโครงการ)
Step 4: Final Presentation & Preliminary Budget (สรุปแบบและงบเบื้องต้น)

หน้า 5: PROFESSIONAL FEE & CONTACT
1. งานส่วน Renovation: [ระบุราคา]
2. งานส่วน Masterplan: [ระบุราคา]
ติดต่อ: [เบอร์โทร/Line ของแจ็ค]
--------------------------------------------------
"""
    
    # 3. ใส่เนื้อหาลงใน Docs
    requests = [{'insertText': {'location': {'index': 1}, 'text': full_text}}]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    
    print(f"URL: https://docs.google.com/document/d/{doc_id}/edit")

if __name__ == '__main__':
    create_doc_proposal()
