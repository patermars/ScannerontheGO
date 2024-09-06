# ScannerontheGO
## Overview

The Video to PDF Converter is a web application that allows users to upload a video file and convert it into a PDF document. It extracts stable frames from the video and compiles them into a multi-page PDF, making it ideal for digitizing printed materials or creating documents from video recordings.

## Features

- Web-based interface for easy video upload
- Automatic extraction of stable frames from video
- Conversion of extracted frames to a multi-page PDF
- Immediate download of the generated PDF

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/patermars/ScannerontheGO
   cd ScannerontheGO
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirments.txt
   ```

## Usage

1. Start the Flask application:
   ```
   python frontend.py
   ```
   OR
   
   Start the Streamlit application:
    ```
    streamlit run frontend_streamlit.py
    ```

3. Open a web browser and navigate to `http://localhost:5000`(flask) or `http://localhost:8501`(streamlit).

4. Use the web interface to upload a video file.

5. After processing, the application will automatically initiate a download of the generated PDF.

## How It Works

1. The user uploads a video through the web interface.
2. The application processes the video, extracting frames at stable points (when the camera isn't moving).
3. These stable frames are then compiled into a multi-page PDF.
4. The resulting PDF is served back to the user for download.

## Contributing

Contributions to improve the Video to PDF Converter are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.

---

Happy converting!
