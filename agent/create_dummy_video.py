import cv2
import numpy as np
import os

def create_test_video(filename="agent/test_video.mp4"):
    width, height = 1280, 720
    fps = 30
    duration = 2  # 2초짜리 영상
    
    # 영상 작성기 설정 (mp4v 코덱 사용)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    for frame_num in range(fps * duration):
        # 파란색 배경 생성
        frame = np.zeros((height, width, 3), np.uint8)
        frame[:] = (255, 0, 0)  # BGR 포맷: 파란색
        
        # 안내 문구 렌더링
        text = "LUNA AGENT - TEST UPLOAD"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        thickness = 5
        color = (255, 255, 255)  # 흰색 텍스트
        
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)
        
        out.write(frame)
        
    out.release()
    print(f"더미 테스트 영상이 성공적으로 생성되었습니다: {filename}")

if __name__ == "__main__":
    create_test_video()
