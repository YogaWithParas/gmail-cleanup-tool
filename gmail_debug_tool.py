import csv
import os
from datetime import datetime

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope for reading and modifying Gmail (including moving emails to Trash)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# File paths (auto-detected from script location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "credentials.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "deletion_log.csv")


# ✅ File check logger
def check_required_files():
    print("\n🔍 Script Directory:", SCRIPT_DIR)
    print(
        "📁 Checking for 'credentials.json'...",
        "✅ Found." if os.path.exists(CREDENTIALS_FILE) else "❌ Not found!",
    )
    print(
        "📁 Checking for 'token.json'...",
        "✅ Found." if os.path.exists(TOKEN_FILE) else "ℹ️ Will be created after login.",
    )


# ✅ Authenticate Gmail
def authenticate_gmail():
    check_required_files()
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    try:
        if not creds or not creds.valid or SCOPES[0] not in creds.scopes:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Expected file '{CREDENTIALS_FILE}' not found in: {SCRIPT_DIR}"
                    )
                print("🔐 Starting OAuth login...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES
                )
                creds = flow.run_local_server(port=0)
                print("✅ Granted scopes:", creds.scopes)

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        print("🔎 Token scopes granted:", creds.scopes)
        return build("gmail", "v1", credentials=creds)

    except RefreshError as e:
        print("🔁 Token refresh failed. Try deleting token.json manually.")
        raise e
    except FileNotFoundError as e:
        print(f"❗ {e}")
        raise e


# 📬 Preview email subjects
def list_email_subjects(service, user_id="me", query=""):
    try:
        response = (
            service.users()
            .messages()
            .list(userId=user_id, q=query, maxResults=10)
            .execute()
        )
        messages = response.get("messages", [])

        if not messages:
            print("📭 No messages found.")
        else:
            print("📨 Email subjects:")
            for msg in messages:
                msg_data = (
                    service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=msg["id"],
                        format="metadata",
                        metadataHeaders=["Subject"],
                    )
                    .execute()
                )
                headers = msg_data["payload"].get("headers", [])
                subject = next(
                    (h["value"] for h in headers if h["name"] == "Subject"),
                    "(No Subject)",
                )
                print("  •", subject)

    except Exception as e:
        print(f"🚫 Failed to list messages: {e}")


# 📒 Log deleted batch
def log_batch_deletion(query: str, deleted_count: int, filename: str = LOG_FILE):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                query,
                deleted_count,
                "Moved to Trash",
                "Used Gmail API with gmail.modify scope",
            ]
        )
    print(f"📝 Deletion log updated → {filename}")


# 🗑️ Move emails to Trash in batches of 1000
MAX_BATCH_SIZE = 1000


def trash_emails(service, user_id, query):
    try:
        message_ids = []
        response = (
            service.users()
            .messages()
            .list(userId=user_id, q=query, maxResults=500)
            .execute()
        )
        if "messages" in response:
            message_ids.extend([msg["id"] for msg in response["messages"]])
        while "nextPageToken" in response:
            response = (
                service.users()
                .messages()
                .list(
                    userId=user_id,
                    q=query,
                    pageToken=response["nextPageToken"],
                    maxResults=500,
                )
                .execute()
            )
            if "messages" in response:
                message_ids.extend([msg["id"] for msg in response["messages"]])

        if message_ids:
            print(f"📦 {len(message_ids)} emails matched the query.")
            for i in range(0, len(message_ids), MAX_BATCH_SIZE):
                batch = message_ids[i : i + MAX_BATCH_SIZE]
                service.users().messages().batchModify(
                    userId=user_id,
                    body={"ids": batch, "removeLabelIds": [], "addLabelIds": ["TRASH"]},
                ).execute()
                print(
                    f"🗑️ Moved batch {i // MAX_BATCH_SIZE + 1} with {len(batch)} emails to Trash."
                )
            log_batch_deletion(query, len(message_ids))
        else:
            print("📭 No messages found to delete.")

    except Exception as e:
        print(f"🚫 Failed to move messages to Trash: {e}")


# ▶️ Main logic
def main():
    service = authenticate_gmail()

    print("\n✅ Gmail API test complete. Now choose an option to delete emails:")
    print("1: Promotions older than 1 year")
    print("2: Social emails older than 1 year")
    print("3: Auto-emails from noreply older than 1 year")
    choice = input("Enter option (1/2/3): ")

    queries = {
        "1": "category:promotions older_than:1y",
        "2": "category:social older_than:1y",
        "3": "from:(noreply@*) older_than:1y",
    }

    if choice in queries:
        list_email_subjects(service, "me", queries[choice])
        confirm = (
            input("\n⚠️ Do you want to move these emails to Trash? (yes/no): ")
            .strip()
            .lower()
        )
        if confirm == "yes":
            trash_emails(service, "me", queries[choice])
        else:
            print("❌ Deletion cancelled.")
    else:
        print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
