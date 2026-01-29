import os
from github import Github
from dotenv import load_dotenv

load_dotenv()


GITHUB_TOKEN = os.environ.get("GITHUB_API_KEY")

g = Github(GITHUB_TOKEN)

try:
	user = g.get_user()
	print(f"Successfully connected to GitHub as: {user.login}")
except Exception as e:
	print(f"ERROR: Unable to connect to GitHub. Please check your API key and permissions.\n{e}")
