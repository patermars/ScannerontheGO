import os
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from generating_pdf import frames_to_pdf
from stable_frames import extract_stable_frames

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
FRAMES_FOLDER = 'frames'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['FRAMES_FOLDER'] = FRAMES_FOLDER


@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)
        
        # Process the video and extract frames
        stable_frames = extract_stable_frames(video_path)
        
        frame_urls = []
        for i, frame in enumerate(stable_frames):
            frame_path = os.path.join(app.config['FRAMES_FOLDER'], f'frame_{i}.png')
            cv2.imwrite(frame_path, frame)
            frame_urls.append(f'/frames/frame_{i}.png')
        
        # Clean up the uploaded video file
        os.remove(video_path)
        
        return jsonify({'frames': frame_urls})

@app.route('/select_frames', methods=['GET'])
def select_frames():
    return render_template('select_frames.html')

@app.route('/frames/<filename>')
def serve_frame(filename):
    return send_file(os.path.join(app.config['FRAMES_FOLDER'], filename))

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    selected_frames = data['selected_frames']
    
    frames = []
    for frame_index in selected_frames:
        frame_path = os.path.join(app.config['FRAMES_FOLDER'], f'frame_{frame_index}.png')
        frames.append(cv2.imread(frame_path))
    
    pdf_filename = 'output.pdf'
    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
    frames_to_pdf(frames, pdf_path)
    
    # Clean up the frames after PDF generation
    for filename in os.listdir(app.config['FRAMES_FOLDER']):
        file_path = os.path.join(app.config['FRAMES_FOLDER'], filename)
        os.remove(file_path)
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
