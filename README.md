# 📬 Gmail Cleanup Tool

A Python script that connects to your Gmail account using the Gmail API and lists subject lines of emails that match predefined filters — like Promotions or Social emails older than 1 year. This tool is designed as a clean, beginner-friendly starter to help you later extend it for deleting, archiving, or labeling emails in bulk.

---

## ⚙️ Features

- ✅ OAuth2 authentication using Google's official libraries
- 📁 Auto-checks for required credential files
- 🔍 Lists subject lines of emails matching your query
- 📦 Modular design for easy extension (delete, archive, etc.)

---

## 🛠️ Requirements

Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt


##📁 Setup
Go to the Google Cloud Console.

Create a new project and enable the Gmail API.

Download credentials.json and place it in the same directory as the script.

Run the script:

bash
Copy
Edit
python gmail_cleanup_tool.py
The first time you run it, you'll be prompted to log in and grant Gmail access. A token.json file will be created for future logins.

##🔍 Query Options
When prompted, choose one of the predefined email queries:

sql
Copy
Edit
1: Promotions older than 1 year
2: Social emails older than 1 year
3: Auto-emails from noreply older than 1 year
You can customize or add more queries in the queries dictionary inside the script.

##🧾 Files Overview
File	Purpose
gmail_cleanup_tool.py	Main script
credentials.json	OAuth2 client secret from Google
token.json	Automatically created after first login
requirements.txt	Python dependencies
.gitignore	Prevents sensitive files from being pushed to GitHub

##🧠 Notes
This script currently only reads email subjects. Extend it to delete or archive emails.

All logic is logged directly in the terminal.

Secure your credentials.json and .gitignore it before uploading to GitHub.

##🙌 Contributing
Pull requests welcome. If you're extending this with new filters or deletion features, feel free to fork and contribute.

##📄 License
MIT

vbnet
Copy
Edit
