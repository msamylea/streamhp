import streamlit as st
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
   
    
    </style
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([0.2, 0.4, 0.4], gap='large')
@st.cache_resource()
def load_forgery():
    from ultralytics import YOLO
    forgery_model = YOLO('models/forgery_detection.onnx', task='classify')
    return forgery_model

with col1:
    with st.container(key='up1'):
        st.html('<h2><u>Upload Known Genuine Signature</h2></u>')
        img1_upload = st.file_uploader(label="", type=["jpg", "jpeg", "png"], key='img1')
    with st.container(key='up2'):
        st.html('<h2><u>Upload Questionable Signature</h2></u>')
        img2_upload = st.file_uploader(label="", type=["jpg", "jpeg", "png"], key='img2')

img_sub = st.button("Submit")

if img_sub:
    if img1_upload and img2_upload:
        with col2:
            with st.spinner("Analyzing signatures..."):
                try:
                    model = load_forgery()
                    combined_img = create_comparison_image(img1_upload, img2_upload)
                    st.subheader("📊 Comparison Analysis")
                    st.divider()

                    st.image(combined_img, caption="Side-by-side signature comparison", width=440)
                    
                    results = model.predict(combined_img)
                    
                    for r in results:
                        prob = r.summary()
                        if prob and len(prob) > 0:
                            pred = prob[0].get('name')
                            confidence = prob[0].get('confidence', 0)
                            conf_format = f"{confidence * 100:.1f}"
                            
                            # Determine colors and icons based on prediction
                            if pred and ('genuine' in pred.lower() or 'authentic' in pred.lower()):
                                ccolor = "#28a745"  # Green
                                icon = "✓"
                                conf_text = "GENUINE"
                            elif pred and ('forg' in pred.lower() or 'fake' in pred.lower()):
                                ccolor = "#dc3545"  # Red
                                icon = "✗"
                                conf_text = "FORGERY"
                            else:
                                ccolor = "#ffc107"  # Yellow
                                icon = "?"
                                conf_text = pred.upper() if pred else "UNCERTAIN"
                            
                            # Confidence interpretation
                            if confidence > 0.8:
                                confidence_text = "High confidence - The model is very certain about this prediction"
                            elif confidence > 0.6:
                                confidence_text = "Medium confidence - The model has reasonable certainty"
                            else:
                                confidence_text = "Low confidence - Consider additional analysis or expert review"
                            
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
                            with col3:
                                st.html(conf_html)
                                
                                # Add balloons for genuine signatures
                                if 'genuine' in pred.lower():
                                    st.balloons()
                        
                        else:
                            st.warning("⚠️ No clear prediction could be made from the analysis")
                            
                except Exception as e:
                    st.error(f"❌ **Error during analysis:** {str(e)}")
                    st.info("💡 Please try with different images or check that both signatures are clearly visible")
    else:
        st.warning("📤 Please upload both signature images before submitting for analysis")