# Importing Neccessary Libraries
import os
import cv2
import numpy as np
from PIL import Image
import streamlit as st
from generating_pdf import frames_to_pdf
from stable_frames import extract_stable_frames


# Define directories for storing uploaded videos, frames, and output PDFs
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
FRAMES_FOLDER = 'frames'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)

# Streamlit title and instructions
st.title("Video to PDF Converter")
st.write("Upload a video file, select frames, and generate a PDF.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

# Process the video only if a file is uploaded and it's not already processed
if uploaded_file is not None and 'video_path' not in st.session_state:
    # Save the uploaded video file
    video_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.video_path = video_path

    # Extract stable frames from the video
    st.write("Processing video...")
    stable_frames = extract_stable_frames(video_path)
    st.session_state.stable_frames = stable_frames

# If frames are already extracted and stored in session state, use them
if 'stable_frames' in st.session_state:
    stable_frames = st.session_state.stable_frames

    # Display extracted frames with checkboxes for selection
    st.write("Select frames to include in the PDF:")
    selected_frames = []

    cols = st.columns(4)  # Create a grid layout with 4 columns

    for i, frame in enumerate(stable_frames):
        frame_path = os.path.join(FRAMES_FOLDER, f'frame_{i}.png')
        cv2.imwrite(frame_path, frame)  # Save each frame as an image
        frame_image = Image.open(frame_path)
        
        with cols[i % 4]:  # Place each frame image in the grid columns
            st.image(frame_image, caption=f"Frame {i + 1}", use_column_width=True)
            # Checkbox to select frames
            if st.checkbox(f"Select Frame {i + 1}", key=f'checkbox_{i}'):
                selected_frames.append(frame)

    # Store selected frames in session state
    st.session_state.selected_frames = selected_frames

    # Button to generate PDF from selected frames
    if st.button("Generate PDF"):
        if st.session_state.selected_frames:
            st.write("Generating PDF...")
            pdf_filename = 'output.pdf'
            pdf_path = os.path.join(OUTPUT_FOLDER, pdf_filename)
            frames_to_pdf(st.session_state.selected_frames, pdf_path)

            # Provide a download link for the generated PDF
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="output.pdf",
                    mime="application/pdf"
                )
        else:
            st.write("No frames selected. Please select at least one frame.")

    # Clean up the uploaded video file after processing
    if 'video_path' in st.session_state:
        os.remove(st.session_state.video_path)
        del st.session_state['video_path']

    # Optionally, clean up the frame images after PDF generation
    for filename in os.listdir(FRAMES_FOLDER):
        file_path = os.path.join(FRAMES_FOLDER, filename)
        os.remove(file_path)
