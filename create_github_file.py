import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

# ดึง Token จาก Environment Variable
GITHUB_TOKEN = os.environ.get("GITHUB_API_KEY")

# สร้าง Object สำหรับเชื่อมต่อกับ GitHub API
g = Github(GITHUB_TOKEN)

# Get Repo
repo = g.get_repo("Archidiot/agdr")

# File name and content
file_name = "test.txt"
file_content = "Hello, this is a test file created by Clawdbot!"

# Create file
try:
    repo.create_file(file_name, "Create test file", file_content)
    print(f"Successfully created {file_name} in the repository.")
except Exception as e:
    print(f"Error creating file: {e}")