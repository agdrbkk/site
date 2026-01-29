import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_API_KEY")
GITHUB_USERNAME = "Archidiot" # แทนค่าด้วย Username ของแจ็ค
REPO_NAME = "agdr" # แทนค่าด้วยชื่อ Repository

# ข้อมูลไฟล์ที่จะสร้าง
file_path = "test.txt"
file_content = "Hello, this is a test file created via Requests!"
commit_message = "Create test file via Requests"

# สร้าง URL สำหรับ GitHub API
url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{file_path}"

# สร้าง Headers (ใส่ Token)
headers = {
"Authorization": f"token {GITHUB_TOKEN}",
"Accept": "application/vnd.github.v3+json"
}

# สร้าง Payload (ข้อมูลที่จะส่งไป)
data = {
"message": commit_message,
"content": file_content.encode("utf-8").decode("utf-8"), # ต้อง encode เป็น base64
"branch": "master" # หรือ "main" ถ้า Repo ใช้ Branch นี้
}

try:
	response = requests.put(url, headers=headers, json=data)
	response.raise_for_status() # Check for HTTP errors

	print(f"Successfully created file: {file_path}")
except requests.exceptions.RequestException as e:
	print(f"Error creating file: {e}")
	print(response.text) # พิมพ์ Error Response จาก GitHub

