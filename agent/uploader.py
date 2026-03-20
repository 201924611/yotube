import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# 이번에는 'youtube.upload' (업로드 권한)을 포함한 SCOPES를 사용합니다.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_service():
    """인증을 처리하고 YouTube API 서비스를 생성합니다."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secrets.json'):
                raise FileNotFoundError("client_secrets.json이 없습니다.")
                
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, file_path, title, description, tags, privacy_status='private'):
    """영상을 유튜브에 업로드합니다."""
    print(f"[{title}] 업로드 준비 중...")
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22' # 22: People & Blogs 등 (대분류)
        },
        'status': {
            'privacyStatus': privacy_status  # 'private', 'unlisted', 'public'
        }
    }

    # 파일 미디어 설정 (chunk size 등 업로드용 통신 설정)
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    print("업로드를 진행합니다. (약간의 시간이 소요될 수 있습니다...)")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"업로드 진행률: {int(status.progress() * 100)}%")

    print(f"✅ 업로드 완료! 영상 ID: {response['id']}")
    video_url = f"https://youtu.be/{response['id']}"
    print(f"🔗 시청 링크: {video_url}")
    
    with open('upload_result.txt', 'w', encoding='utf-8') as f:
        f.write(video_url)

if __name__ == "__main__":
    video_path = "agent/test_video.mp4"
    if not os.path.exists(video_path):
        print("에러: 업로드할 테스트 영상이 존재하지 않습니다.")
    else:
        try:
            youtube_service = get_youtube_service()
            upload_video(
                youtube=youtube_service,
                file_path=video_path,
                title="[테스트] 루나 에이전트의 첫 번째 자동 업로드 테스트",
                description="이 영상은 Python 스크립트와 YouTube Data API를 통해 생성 및 업로드된 더미 영상입니다.",
                tags=["테스트", "자동화", "에이전트"],
                privacy_status="private" # 보안을 위해 비공개 설정
            )
        except Exception as e:
            print(f"업로드 중 에러 발생: {e}")
