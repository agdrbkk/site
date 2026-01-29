import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

# ดึง Token จาก Environment Variable
GITHUB_TOKEN = os.environ.get("GITHUB_API_KEY")

# สร้าง Object สำหรับเชื่อมต่อกับ GitHub API
g = Github(GITHUB_TOKEN)

# Get User
user = g.get_user()

# สร้าง Repository ใหม่
repo_name = "agdr"
repo_description = "Portfolio website for ALL GROUP DESIGN AND RESEARCH"

try:
    user.create_repo(repo_name, description=repo_description, private=False)
    print(f"Successfully created repository: {repo_name}")
except Exception as e:
    print(f"Error creating repository: {e}")