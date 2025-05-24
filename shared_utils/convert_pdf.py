from pdf2image import convert_from_bytes

import io


def handle_pdf(pdf_file, dpi=200, fmt="jpeg", quality=75):
    """
    Convert PDF bytes to a list of JPEG image buffers.
    
    Args:
        pdf_file (bytes): The PDF file content as bytes
        dpi (int): DPI resolution for the images (higher = better quality but larger files)
        fmt (str): Image format ('jpeg' or 'png')
        quality (int): JPEG quality (1-100, higher = better quality but larger files)
        
    Returns:
        list: List of image byte buffers
    """
    # Convert PDF to images
    try:
        pdf_images = convert_from_bytes(
            pdf_file, 
            dpi=dpi,
            fmt=fmt
        )
        
        # Create list to store image buffers
        image_buffers = []
        
        # Convert each image to bytes and store in list
        for i, img in enumerate(pdf_images):
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            buffer.seek(0)  # Reset buffer position to start
            image_buffers.append(buffer.getvalue())
            
        return image_buffers
        
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        return []