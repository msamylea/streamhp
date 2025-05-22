import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
import numpy as np
import torch

torch.classes.__path__ = []

# Page header
st.title("📄 Signature Detection")
st.markdown("Upload a PDF document to automatically detect and extract signatures")

st.markdown(
    """
    <style>
    .st-key-sig-card {
        background: white;
        border: 2px solid red;
        color: black;
        display: flex;
        justify-content: center;
        padding: 20px;
        border-radius: 10px;
        
    }
    
    .st-key-sig3-card {
        background: white;
        border: 2px solid red;
        color: black;
        display: flex;
        justify-content: center;
        padding: 20px;
        border-radius: 10px;
        
    }
    
        .st-key-sig2-card {
        background: white;
        border: 2px solid red;
        color: black;
        display: flex;
        justify-content: center;
        padding: 20px;
        border-radius: 10px;
        
    }
    
    div .stDownloadButton {
        background: black;
        color: white;
        font-size: 12px;
    }
    

     </style
    """,
    unsafe_allow_html=True
)

@st.cache_resource()
def load_signature():
    from ultralytics import YOLO

    sig_model = YOLO('models/sig_detect.onnx')
    return sig_model

# Upload section
col1, col2 = st.columns([1, 2], gap='large')

with col1:
    st.subheader("📤 Upload Document")
    pdf_uploader = st.file_uploader(
        "Choose a PDF file", 
        type="pdf",
        help="Upload a PDF document containing signatures to detect"
    )
    
    if pdf_uploader:
        st.success(f"✅ Uploaded: {pdf_uploader.name}")
        submit_btn = st.button("🔍 Analyze Document", type="primary", use_container_width=True)
    else:
        submit_btn = False

with col2:
    if not pdf_uploader:
        st.info("""
        ### 📋 Instructions:
        1. Upload a PDF document using the file uploader
        2. Click "Analyze Document" to detect signatures
        3. View detected signatures and extracted crops
        
        **Supported formats:** PDF files only
        """)
    elif submit_btn and pdf_uploader is not None:
        with st.spinner("Converting PDF and analyzing signatures..."):
            pdf_images = convert_from_bytes(
                pdf_uploader.getvalue(), 
                dpi=200,
                fmt='jpeg'
            )
            
            # Load model
            model = load_signature()
            
            # Summary metrics
            total_signatures = 0
            total_pages = len(pdf_images)
            
            with st.container(key='sig-card'):
                
                st.subheader("📊 Analysis Results")
                st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#808080;" /> """, unsafe_allow_html=True) 

                st.write("---")
                
                # Process each page
                for page_num, img in enumerate(pdf_images):
                    st.markdown(f"#### Page {page_num + 1}:")
                    
                    # Run prediction
                    prediction = model.predict(img)
                    
                    for p in prediction:
                        boxes = p.boxes
                        page_signatures = len(boxes)
                        total_signatures += page_signatures
                        
                        if page_signatures == 0:
                            st.warning(f"No signatures detected")
                            st.image(img, caption=f"Page {page_num + 1}:", width=300)
                        else:
                            st.markdown(f"##### ***Found {page_signatures} signature(s)***")
                            
                            # Show detection results
                            st.markdown("##### Detections:")
                            st.image(p.plot(), width=400)
                            
            with st.container(key='sig2-card'):
                st.subheader("✂️ Extracted Signatures:")
                st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#808080;" /> """, unsafe_allow_html=True) 

                st.write("---")
                # Extract and display crops
                img_array = np.array(img)
                
                for i, box in enumerate(boxes):
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    
                    # Crop the image
                    cropped = img_array[y1:y2, x1:x2]
                    crop_img = Image.fromarray(cropped)
                    
                    st.image(crop_img, caption=f"Signature {i+1}", width=200)
                    
                    # Download button
                    img_buffer = BytesIO()
                    crop_img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    
                    st.download_button(
                        label=f"Download Signature {i+1}",
                        data=img_buffer.getvalue(),
                        file_name=f"signature_page{page_num+1}_sig{i+1}.png",
                        mime="image/png",
                        key=f"download_{page_num}_{i}",
                    )
                    
                    st.markdown("---")
        with st.container(key='sig3-card'):

            # Summary metrics
            st.subheader("📊 Summary:")
            st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#808080;" /> """, unsafe_allow_html=True) 
            st.write("---")
            st.write(f"##### Total Pages: {total_pages}")
            st.write(f"##### Total Signatures: {total_signatures}")
            avg_sigs = round(total_signatures / total_pages, 1) if total_pages > 0 else 0
            st.write(f"##### Avg. Signatures/Page: {avg_sigs}")
            
            if total_signatures > 0:
                st.markdown("##### ***Analysis complete!***")
            else:
                st.markdown("#### ***No signatures detected.***")