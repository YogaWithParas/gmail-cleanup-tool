import json

with open("credentials.json", "r") as f:
    creds = json.load(f)

with open(".env", "w") as env_file:
    env_file.write(f"GMAIL_CLIENT_ID={creds['installed']['client_id']}\n")
    env_file.write(f"GMAIL_CLIENT_SECRET={creds['installed']['client_secret']}\n")

print("✅ .env file generated successfully.")
