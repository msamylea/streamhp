from PIL import Image

def create_comparison_image(img1_path, img2_path):
    # Open images
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    
    # Resize to same height
    height = max(img1.height, img2.height)
    width1 = int(img1.width * (height / img1.height))
    width2 = int(img2.width * (height / img2.height))
    
    img1 = img1.resize((width1, height), Image.LANCZOS)
    img2 = img2.resize((width2, height), Image.LANCZOS)
    
    # Create new image with space for both images
    total_width = width1 + width2
    comparison = Image.new('RGB', (total_width, height))
    
    # Paste images side by side
    comparison.paste(img1, (0, 0))
    comparison.paste(img2, (width1, 0))
    
    return comparison