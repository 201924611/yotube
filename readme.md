youtube 자동 업로드 에이전트
1. 현재 핫한 키워드 분석
2. 업로드 후 영상 조회수 분석
3. 조회수가 잘 나오지 않으면 머가 문제인지
4. 문제점 분석 후 개선
5. 개선 후 다시 업로드

---

## 🚀 로컬 환경 설정 및 실행 방법 (Getting Started)

### 1. 파이썬 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows)
.venv\Scripts\activate
# 가상환경 활성화 (Mac/Linux)
# source .venv/bin/activate
```

### 2. 필수 라이브러리(패키지) 설치
```bash
pip install -r requirements.txt
```
**. 핫한 유튜브 트렌드 키워드 분석하기**
```bash
python agent/trend_analyzer.py
```
> 첫 실행 시 웹 브라우저가 열리며 Google 계정 로그인을 요구합니다. 인증을 수락해 주세요.

**. (테스트) 임시 2초 더미 영상 렌더링 후 비공개 업로드하기**
```bash
python agent/create_dummy_video.py
python agent/uploader.py
```
> 업로드 권한이 새롭게 필요하므로 인증 브라우저가 다시 열립니다. 승인하면 유튜브 채널에 비공개로 테스트 영상이 올라갑니다.