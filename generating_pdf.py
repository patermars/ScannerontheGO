import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image
import io


def frames_to_pdf(frames, output_path):
    # Determine page size based on the first frame
    img = Image.fromarray(cv2.cvtColor(frames[0], cv2.COLOR_BGR2RGB))
    width, height = img.size

    # Create a new PDF with ReportLab
    c = canvas.Canvas(output_path, pagesize=(width, height))

    for idx, frame in enumerate(frames):
        # Convert OpenCV BGR to RGB
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Create a new page
        if idx > 0:
            c.showPage()

        # Add the image to the PDF
        c.drawInlineImage(img, 0, 0, width, height)

    # Save the PDF
    c.save()