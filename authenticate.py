from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# 🔹 OAuth 認証情報の設定
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "token.json"  # ✅ 認証トークンを保存（次回以降の認証不要）
SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]

def authenticate_youtube():
    """
    ローカル環境で OAuth 認証を行い、トークンをキャッシュする
    """
    credentials = None

    # 🔹 既存のトークンがあれば、それを使用（再認証不要）
    if os.path.exists(TOKEN_FILE):
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials

        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 🔹 トークンがない場合、新規認証
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)  # ✅ ローカル環境ならブラウザ認証が可能

        # 🔹 認証トークンを保存（次回から自動ログイン）
        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    youtube_analytics = build("youtubeAnalytics", "v2", credentials=credentials)
    return youtube_analytics

# 🔹 認証を実行
if __name__ == "__main__":
    youtube_analytics = authenticate_youtube()
    print("✅ 認証成功！YouTube Analytics API にアクセスできます。")