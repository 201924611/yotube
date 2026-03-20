import os
import re
from collections import Counter
from pytrends.request import TrendReq
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_youtube_service():
    """인증을 처리하고 YouTube API 서비스를 생성합니다."""
    creds = None
    # 토큰 파일이 있으면 인증 정보를 불러옵니다.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 인증 정보가 없거나 만료되었을 경우 새롭게 인증을 진행합니다.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secrets.json'):
                raise FileNotFoundError('client_secrets.json 파일을 찾을 수 없습니다.')
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 인증을 성공하면 다음 번 실행을 위해 토큰을 저장합니다.
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)


def fetch_youtube_trends(youtube, region_code='KR', max_results=20):
    """YouTube 인기 급상승 동영상 목록에서 키워드를 추출합니다."""
    print(f"[YouTube] {region_code} 지역 인기 급상승 영상 수집 중...")
    
    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()

    titles = []
    tags = []
    
    for item in response.get('items', []):
        snippet = item['snippet']
        titles.append(snippet.get('title', ''))
        tags.extend(snippet.get('tags', []))
        
    return titles, tags


def fetch_google_trends(region='south_korea'):
    """Google Trends에서 일일 인기 검색어를 가져옵니다."""
    print(f"[Google Trends] {region} 일일 인기 검색어 수집 중...")
    try:
        pytrends = TrendReq(hl='ko-KR', tz=540)
        # 일별 인기 검색어 (한국)
        trending_searches_df = pytrends.trending_searches(pn=region)
        return trending_searches_df[0].tolist()
    except Exception as e:
        print(f"Google Trends 수집 중 오류 발생: {e}")
        return []


def analyze_keywords(youtube_titles, youtube_tags, google_trends):
    """수집된 데이터에서 핫한 키워드들을 추출하고 분석합니다."""
    print("\n[Analysis] 종합 키워드 분석 시작...")
    
    # 1. 텍스트 정제 함수 (특수문자 제거, 띄어쓰기 기준 단어 분리)
    def extract_words(text_list):
        words = []
        for text in text_list:
            # 특수문자 제거 및 소문자 변환
            cleaned = re.sub(r'[^\w\s\uAC00-\uD7A3]', ' ', text).lower()
            # 1글자 이상의 의미 있는 단어만 추출
            for word in cleaned.split():
                if len(word) > 1:
                    words.append(word)
        return words

    # 2. YouTube 제목 단어 추출
    youtube_words = extract_words(youtube_titles)
    
    # 3. 빈도수 카운트
    word_counts = Counter(youtube_words)
    tag_counts = Counter(youtube_tags)
    
    print("\n========== [트렌드 리포트] ==========")
    
    print("\n👉 [Google Trends 인기 검색어 TOP 10]")
    for i, keyword in enumerate(google_trends[:10], 1):
        print(f"{i}. {keyword}")
        
    print("\n👉 [YouTube 인기 상승 타이틀 빈출 단어 TOP 20]")
    for word, count in word_counts.most_common(20):
        if not word.isdigit(): # 단순 숫자는 제외
            print(f"- {word} ({count}회)")
            
    print("\n👉 [YouTube 인기 상승 태그 TOP 10]")
    for tag, count in tag_counts.most_common(10):
        print(f"- {tag} ({count}회)")
        
    print("\n=====================================")


if __name__ == "__main__":
    try:
        # YouTube 데이터 수집
        youtube_service = get_youtube_service()
        titles, tags = fetch_youtube_trends(youtube_service)
        
        # Google Trends 데이터 수집
        g_trends = fetch_google_trends()
        
        # 분석 결과 출력
        analyze_keywords(titles, tags, g_trends)
        
    except FileNotFoundError as e:
        print(f"에러: {e}")
        print("유튜브 API 'client_secrets.json' 파일을 프로젝트 최상단 폴더에 넣어주세요.")
    except Exception as e:
        print(f"실행 중 예기치 못한 에러가 발생했습니다: {e}")
