from stable_frames import extract_stable_frames
from generating_pdf import frames_to_pdf


#sample use case
video_path = 'Test.mp4'
stable_frames = extract_stable_frames(video_path)

# Process stable frames (apply image processing, OCR, etc.)
for idx, frame in enumerate(stable_frames):
    # Save frame as image
    cv2.imwrite(f'frames/stable_frame_{idx}.jpg', frame)

frames_to_pdf(stable_frames, "newpdf.pdf")