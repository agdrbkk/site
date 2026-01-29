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

# List Repositories
for repo in user.get_repos():
    print(repo.name)
