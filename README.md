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

## 📁 Setup

1. Create a project in the Google Cloud Console and enable the Gmail API.
2. Place `credentials.json` next to the script.
3. Run:

```bash
python gmail_debug_tool.py
```

The first run prompts you to log in and creates `token.json`.

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
