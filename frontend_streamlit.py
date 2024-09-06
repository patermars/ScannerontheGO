import os
import streamlit as st
import cv2
import numpy as np
from generating_pdf import frames_to_pdf
from stable_frames import extract_stable_frames
from PIL import Image

# Directories
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
FRAMES_FOLDER = 'frames'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)

# Streamlit title and instructions
st.title("Video to PDF Converter")
st.write("Upload a video file, select frames, and generate a PDF.")

# File uploader
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    # Save uploaded file
    video_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process the video and extract frames
    st.write("Processing video...")
    stable_frames = extract_stable_frames(video_path)

    # Display extracted frames for selection
    st.write("Select frames to include in the PDF:")
    selected_frames = []
    frame_images = []
    
    for i, frame in enumerate(stable_frames):
        frame_path = os.path.join(FRAMES_FOLDER, f'frame_{i}.png')
        cv2.imwrite(frame_path, frame)
        frame_image = Image.open(frame_path)
        frame_images.append(frame_image)
        if st.checkbox(f"Select Frame {i + 1}", key=i):
            selected_frames.append(frame)

    if st.button("Generate PDF"):
        if selected_frames:
            st.write("Generating PDF...")
            pdf_filename = 'output.pdf'
            pdf_path = os.path.join(OUTPUT_FOLDER, pdf_filename)
            frames_to_pdf(selected_frames, pdf_path)

            # Provide a download link for the PDF
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="output.pdf",
                    mime="application/pdf"
                )
        else:
            st.write("No frames selected. Please select at least one frame.")

    # Clean up the uploaded video file
    os.remove(video_path)

    # Optionally, clean up the frames after PDF generation
    for filename in os.listdir(FRAMES_FOLDER):
        file_path = os.path.join(FRAMES_FOLDER, filename)
        os.remove(file_path)
