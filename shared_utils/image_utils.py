# image_utils.py
"""Image processing utilities without OpenCV dependency"""

import numpy as np
from skimage import measure, morphology
from PIL import Image, ImageChops, ImageEnhance, ImageDraw

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
    
    def apply_morphology(self,mask, kernel_size=5):
        """Apply erosion and dilation to clean up the mask."""
        # Convert to binary
        binary_mask = mask > 127
        
        # Create structuring element (disk-shaped kernel)
        selem = morphology.disk(kernel_size // 2)
        
        # Erosion followed by dilation (opening operation)
        eroded = morphology.binary_erosion(binary_mask, selem)
        dilated = morphology.binary_dilation(eroded, selem)
        
        return (dilated * 255).astype(np.uint8)


    def find_and_mark_regions(self, original_image, mask, min_area=50):
        """Find contours and draw bounding boxes on suspicious areas."""
        # Convert mask to binary
        binary_mask = mask > 127
        
        # Label connected components
        labeled_mask = measure.label(binary_mask)
        regions = measure.regionprops(labeled_mask)
        
        # Create a copy of the image to draw on
        marked_image = original_image.copy()
        draw = ImageDraw.Draw(marked_image)
        
        suspicious_areas = []
        
        for region in regions:
            # Check if area is large enough
            if region.area > min_area:
                # Get bounding box coordinates
                minr, minc, maxr, maxc = region.bbox
                x, y, w, h = minc, minr, maxc - minc, maxr - minr
                
                suspicious_areas.append((x, y, w, h))
                
                # Draw rectangle on image
                draw.rectangle(
                    [x, y, x + w, y + h],
                    outline=(0, 255, 0),
                    width=2
                )
        
        return suspicious_areas, marked_image
        
    def detect_highlighted_areas(self, image_input):
        """Simplified version using PIL's HSV conversion."""
        # Handle different input types
        if isinstance(image_input, np.ndarray):
            # If it's already a numpy array
            image = Image.fromarray(image_input)
        elif isinstance(image_input, Image.Image):
            # If it's already a PIL Image
            image = image_input
        elif isinstance(image_input, str):
            # If it's a file path string
            image = Image.open(image_input)
        else:
            # Try to open it as a file-like object
            try:
                image = Image.open(image_input)
            except:
                # If all else fails, assume it's already an image
                image = image_input
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to HSV using PIL
        hsv_image = image.convert('HSV')
        hsv_array = np.array(hsv_image)
        
        # Note: PIL's HSV scale is different (H: 0-255, S: 0-255, V: 0-255)
        # So we need to adjust the bounds
        pil_lower_bound = np.array([
            int(self.lower_bound[0] * 255 / 179),  # Convert H from 0-179 to 0-255
            self.lower_bound[1],  # S stays the same
            self.lower_bound[2]   # V stays the same
        ])
        pil_upper_bound = np.array([
            int(self.upper_bound[0] * 255 / 179),
            self.upper_bound[1],
            self.upper_bound[2]
        ])
        
        # Create mask
        mask = np.all(
            (hsv_array >= pil_lower_bound) & (hsv_array <= pil_upper_bound),
            axis=2
        ).astype(np.uint8) * 255
        
        # Apply morphology and find regions
        mask_cleaned = self.apply_morphology(mask, kernel_size=5)
        suspicious_areas, marked_image = self.find_and_mark_regions(
            image, mask_cleaned, min_area=50
        )
        
        return suspicious_areas, marked_image
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
            