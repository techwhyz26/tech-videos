"""One-time YouTube sign-in. Run it on your own PC:

    python tools/youtube_auth.py path\\to\\client_secret.json
    python tools/youtube_auth.py          (asks you to paste the Client ID and secret instead)

It opens Google's sign-in page in your browser. Choose the TechWhyz channel and allow uploads. The
script then saves YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET and YOUTUBE_REFRESH_TOKEN as GitHub secrets of
the repository (through the GitHub CLI) without printing them.
"""
from __future__ import annotations

import http.server
import json
import secrets
import shutil
import subprocess
import sys
import urllib.parse
import webbrowser
from pathlib import Path

import httpx

REPO = "techwhyz26/tech-videos"
SCOPE = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly"


def gh() -> str:
    for candidate in (shutil.which("gh"), r"C:\Program Files\GitHub CLI\gh.exe"):
        if candidate and Path(candidate).exists():
            return candidate
    sys.exit("GitHub CLI (gh) was not found.")


def save_secret(name: str, value: str) -> None:
    subprocess.run([gh(), "secret", "set", name, "-R", REPO], input=value.encode(), check=True)


def main() -> None:
    if len(sys.argv) == 2 and Path(sys.argv[1]).is_file():
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        client = data.get("installed") or data.get("web") or {}
        client_id, client_secret = client.get("client_id"), client.get("client_secret")
    else:  # no JSON file: paste the two values from the Google Cloud client page
        import getpass
        client_id = input("Paste the Client ID and press Enter: ").strip()
        client_secret = getpass.getpass("Paste the Client secret (it stays hidden) and press Enter: ").strip()
    if not client_id or not client_secret:
        sys.exit("That file has no client_id/client_secret. Download the OAuth client JSON (Desktop app).")

    result: dict[str, str] = {}
    state = secrets.token_urlsafe(16)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if query.get("state", [""])[0] == state:
                result["code"] = query.get("code", [""])[0]
                result["error"] = query.get("error", [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h2>Done. You can close this tab and go back to the terminal.</h2>".encode())

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    redirect = f"http://127.0.0.1:{server.server_port}"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": client_id, "redirect_uri": redirect, "response_type": "code", "scope": SCOPE,
        "access_type": "offline", "prompt": "consent", "state": state})
    print("Opening Google sign-in in your browser. If it does not open, paste this link into it:\n" + url)
    webbrowser.open(url)
    while "code" not in result:
        server.handle_request()
    if result.get("error") or not result.get("code"):
        sys.exit(f"Sign-in was cancelled or refused: {result.get('error')}")

    r = httpx.post("https://oauth2.googleapis.com/token", data={
        "code": result["code"], "client_id": client_id, "client_secret": client_secret,
        "redirect_uri": redirect, "grant_type": "authorization_code"}, timeout=60)
    tokens = r.json()
    if "refresh_token" not in tokens:
        sys.exit(f"Google did not return a refresh token: {tokens.get('error_description') or tokens}")

    me = httpx.get("https://www.googleapis.com/youtube/v3/channels", params={"part": "snippet", "mine": "true"},
                   headers={"Authorization": f"Bearer {tokens['access_token']}"}, timeout=60).json()
    items = me.get("items") or []
    print("Signed in to channel:", items[0]["snippet"]["title"] if items else "(no channel found!)")

    save_secret("YOUTUBE_CLIENT_ID", client_id)
    save_secret("YOUTUBE_CLIENT_SECRET", client_secret)
    save_secret("YOUTUBE_REFRESH_TOKEN", tokens["refresh_token"])
    print("Saved YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET and YOUTUBE_REFRESH_TOKEN to GitHub. All done.")


if __name__ == "__main__":
    main()
