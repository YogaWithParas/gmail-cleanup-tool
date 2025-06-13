"""Manual script to test Gmail OAuth authentication.

This module isn't meant to be imported during automated test runs.
It now guards the OAuth flow so pytest can safely import the file
without requiring the Google API libraries or network access.
"""

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def main() -> None:
    # Import locally to avoid dependency issues when the module is imported by
    # automated test runners.
    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

    print("Authorization successful. Token saved.")


if __name__ == "__main__":  # pragma: no cover - manual invocation only
    main()
