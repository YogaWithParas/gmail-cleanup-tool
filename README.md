# 📬 Gmail Cleanup Tool

This repository provides a small Python script that connects to Gmail, lists matching messages and can move them to Trash. It's intended as a minimal starting point for bulk email cleanup.

---

## ⚙️ Features

- OAuth2 authentication using Google's official libraries
- Auto-checks for required credential files
- Lists subject lines for common queries
- Modular design for easy extension

---

## 🛠️ Requirements

Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔐 Gmail API Setup Instructions

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Gmail API**.
3. Under "OAuth consent screen", configure the application as Internal or External.
4. Under "Credentials" → Create credentials → OAuth Client ID → Select **Desktop App**.
5. Download the `credentials.json` file and place it in the root folder of this project.
6. Run the script — it will authenticate and create a `token.json` file on first run.

⚠️ **Do not share your credentials.json or token.json.**
They contain sensitive information and are user-specific.

## 🔍 Query Options

When prompted, choose one of the predefined queries:

```
1: Promotions older than 1 year
2: Social emails older than 1 year
3: Auto-emails from noreply older than 1 year
```

You can customize or add more queries in `gmail_debug_tool.py`.

## 🧾 Files Overview

| File | Purpose |
|---|---|
| `gmail_debug_tool.py` | Main script |
| `credentials.json` | OAuth2 client secret from Google |
| `token.json` | Created after first login |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Prevents sensitive files from being committed |

## 🧠 Notes

The script currently only lists email subjects. Extend it to delete or archive emails. All actions are logged in the terminal.

## 🙌 Contributing

Pull requests are welcome.

## 📄 License

MIT
