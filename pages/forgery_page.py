import streamlit as st
from transformers import pipeline
from PIL import Image


from utils.combine_imgs import create_comparison_image
from datetime import datetime
import torch

torch.classes.__path__ = []

st.markdown(
    """
    <style>
    .st-key-up1 {
        background: white;
        border: 2px solid red;
        font-size: 10px;
        color: black;
        display: flex;
        align-items: left;
        justify-content: center;
        padding: 5px;
        border-radius: 10px;
        
    }
    
    .st-key-up2 {
        background: white;
        border: 2px solid red;
        font-size: 10px;
        color: black;
        display: flex;
        align-items: centlefter;
        justify-content: center;
        padding: 5px;
        border-radius: 10px;
        
    }
    div[data-testid="stFileUploader"] {
        background: green;
        border-radius: 20px;
    }
    .workflow-step {
        background: #e4f4e8;
        color: black;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-bottom: 15px;
    }
    
   
    </style
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns([0.2, 0.2, 0.3, 0.3], gap='small')


@st.cache_resource()
def load_forgery():
    from ultralytics import YOLO
    forgery_model = YOLO('models/forgery_detection.onnx', task='classify')
    return forgery_model

with col1:
    # with st.container(key='up1'):
        st.markdown("""
                                  
                    <div class="workflow-step">
                        <strong>Upload Known Genuine Signature.</strong>
                    </div>

                    """, unsafe_allow_html=True)
        img1_upload = st.file_uploader(label="x", type=["jpg", "jpeg", "png"], key='img1', label_visibility='hidden')
with col2:
        st.markdown("""
                                  
                    <div class="workflow-step">
                        <strong>Upload Questioned Signature.</strong>
                    </div>

                    """, unsafe_allow_html=True)
        img2_upload = st.file_uploader(label="x", type=["jpg", "jpeg", "png"], key='img2', label_visibility='hidden')

img_sub = st.button("Submit", type='primary')

if img_sub:
    if img1_upload and img2_upload:
        with col3:
            with st.spinner("Analyzing signatures..."):
                try:
                    # model = load_forgery()
                    model = pipeline("image-classification",'aevalone/vit-base-patch16-224-finetuned-forgery')
                    combined_img = create_comparison_image(img1_upload, img2_upload)
                    st.subheader("📊 Comparison Analysis")
                    st.divider()

                    st.image(combined_img, caption="Side-by-side signature comparison", width=440)
                    try:
                        results = model(combined_img)
                    except Exception as e:
                        st.write(f"error during HF Model step {e}")
                    
                    for r in results:
                        for key, value in r.items():
                            if value == 'forgery':
                                fscore = r.get('score')
                            if value == 'genuine':
                                gscore = r.get('score')
                                

                    if gscore > fscore:
                        final_result = "Genuine"
                        final_score = gscore
                        ccolor = "#28a745"  # Green
                        icon = "✓"
                        conf_text = "GENUINE"

                    elif fscore > gscore:
                        final_result = "Forged"
                        final_score = fscore
                        ccolor = "#dc3545"  # Red
                        icon = "✗"
                        conf_text = "FORGERY"

                    else:
                        ccolor = "#ffc107"  # Yellow
                        icon = "?"
                        conf_text = "UNCERTAIN"
                    
                    # Confidence interpretation
                    if final_score > 0.8:
                        confidence_text = "High confidence - The model is very certain about this prediction"
                    elif final_score > 0.6:
                        confidence_text = "Medium confidence - The model has reasonable certainty"
                    else:
                        confidence_text = "Low confidence - Consider additional analysis or expert review"
                    
                    conf_format = f"{final_score * 100:.1f}"
                    # Custom HTML
                    conf_html = f"""
                    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 400px; margin: 20px auto; 
                                padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                                background: #f8f9fa;">
                        <h2 style="text-align: center; color: #343a40; margin-top: 0;">Signature Verification</h2>
                        <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(0,0,0,0.2), rgba(0,0,0,0));">
                        
                        <div style="display: flex; align-items: center; justify-content: center; margin: 25px 0;">
                            <div style="width: 80px; height: 80px; border-radius: 50%; background-color: {ccolor}; 
                                    display: flex; align-items: center; justify-content: center; color: white; 
                                    font-size: 38px; font-weight: bold;">{icon}</div>
                        </div>
                        
                        <div style="text-align: center; margin: 20px 0;">
                            <h3 style="font-size: 24px; margin-bottom: 5px; color: {ccolor};">{conf_text}</h3>
                            <p style="font-size: 18px; margin-top: 5px; color: #6c757d;">
                                with <span style="color: {ccolor}; font-weight: bold;">{conf_format}%</span> confidence
                            </p>
                        </div>
                        
                        <div style="background-color: rgba(0,0,0,0.05); border-radius: 5px; padding: 10px; margin-top: 15px;">
                            <p style="margin: 0; color: #6c757d; font-size: 14px;">
                                <strong>Confidence Level:</strong> {confidence_text}
                            </p>
                            <div style="height: 6px; background-color: #e9ecef; border-radius: 3px; margin-top: 8px;">
                                <div style="width: {conf_format}%; height: 100%; background-color: {ccolor}; border-radius: 3px;"></div>
                            </div>
                        </div>
                        
                        <div style="margin-top: 20px; font-size: 12px; color: #adb5bd; text-align: center;">
                            Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        </div>
                    </div>
                    """
                    with col4:
                        st.html(conf_html)
                        
                        # Add balloons for genuine signatures
                        if 'genuine' in final_result.lower():
                            st.balloons()
                
                   
                            
                except Exception as e:
                    st.error(f"❌ **Error during analysis:** {str(e)}")
                    st.info("💡 Please try with different images or check that both signatures are clearly visible")
    # else:
    #     st.warning("📤 Please upload both signature images before submitting for analysis")