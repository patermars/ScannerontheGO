import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def extract_stable_frames(video_path, similarity_threshold=0.90, stability_duration=0.5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    prev_frame = None
    stable_frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            similarity = ssim(prev_frame, gray)
            if similarity > similarity_threshold:
                stable_frames.append(frame)

        prev_frame = gray

    cap.release()
    return stable_frames

def main():
# Usage
video_path = 'Test.mp4'
stable_frames = extract_stable_frames(video_path)

# Process stable frames (apply image processing, OCR, etc.)
for idx, frame in enumerate(stable_frames):
    # Save frame as image
    cv2.imwrite(f'frames/stable_frame_{idx}.jpg', frame)
    
    # TODO: Add image processing and OCR steps here

if __name__ == "__main__":
    main()