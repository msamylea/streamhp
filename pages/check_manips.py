import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageChops, ImageEnhance
from utils.extract_versions import analyze_pdf_versions, display_diff_summary
import torch

torch.classes.__path__ = []

col1, col2 = st.columns([0.3, 0.7], gap='large')

class ModdedDocAnalyzer:
    def __init__(self):
        self.lower_bound = np.array([0, 10, 10])
        self.upper_bound = np.array([179, 255, 245])
    
    def convert_to_ela_image(self, image, quality=90):
        """Performs Error Level Analysis on an image."""
        # image = Image.open(image_path).convert('RGB')
        temp_image = image.copy()
        temp_image.save("temp.jpg", quality=quality)
        temp_image = Image.open("temp.jpg")
        
        ela_image = ImageChops.difference(image, temp_image)
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1
        scale = 255.0 / max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        return ela_image
    
    def highlight_deviations(self, ela_image, threshold=20):
        """Highlights deviations in an ELA image based on a threshold."""
        ela_array = np.array(ela_image)
        mask = (ela_array > threshold).astype(np.uint8) * 255
        return Image.fromarray(mask)
    
    def detect_highlighted_areas(self, image_path):
        """Detect and mark suspicious areas in the image."""
        
        img = np.asarray(image_path)
        _, encoded_image = cv2.imencode('.jpg', img)
        image_bytes = encoded_image.tobytes()
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.COLOR_BGR2HSV)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        
        # Morphological operations for noise reduction
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        suspicious_areas = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:
                x, y, w, h = cv2.boundingRect(contour)
                suspicious_areas.append((x, y, w, h))
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        return suspicious_areas, image
    
    def analyze_pdf(self, manip_uploader):
        """Perform complete deepfake analysis on a PDF."""
        # Convert PDF to image
        from pdf2image import convert_from_bytes
        image = convert_from_bytes(manip_uploader.getvalue(), dpi=300, use_pdftocairo=True)
       
        for img in image:
            # Perform ELA analysis
            ela_image = self.convert_to_ela_image(img, quality=90)
            
            # Detect suspicious areas
            deviation = self.highlight_deviations(ela_image, threshold=20)

            # Find and mark suspicious areas
            suspicious_areas, marked_image = self.detect_highlighted_areas(ela_image)
            
            results = {
                "suspicious_areas_count": len(suspicious_areas),
                "suspicious_areas": suspicious_areas,
                "images": {
                    "original": image[0],
                    "ela_analysis":ela_image,
                    "deviation_mask": deviation,
                    "marked_areas":marked_image
                }
            }
            
            return results
            
analyzer = ModdedDocAnalyzer()

st.markdown(
    """
    <style>
    .st-key-manip-card {
        background: white;
        border: 2px solid red;
        color: black;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        border-radius: 10px;
        
    }
    
    .st-key-version-card {
        background: white;
        border: 2px solid red;
        color: black;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        border-radius: 10px;
        
    }
    </style
    """,
    unsafe_allow_html=True
)

with col1:
    manip_uploader = st.file_uploader(label="Upload PDF File", type="pdf", accept_multiple_files=False)
    manip_submit = st.button("Submit")

with col2:
    c1, c2 = st.columns(2)
    if manip_submit:
        if manip_uploader:
            with c1:
                result = analyzer.analyze_pdf(manip_uploader)

                result_img = result.get('images').get('deviation_mask')
                with st.container(key='manip-card'):
                    st.markdown("### Detection Results")
                    st.divider()
                    st.markdown('***Image manipulations will show up as highlighted areas in the image if any exist. If no manipulations were found, no highlights will appear***')
                    st.divider()
                    st.image(result_img)
            with c2:
                result = analyze_pdf_versions(manip_uploader)
                with st.container(key='version-card'):
                    display_diff_summary(result.get('diffs'))