import streamlit as st
from transformers import pipeline


from shared_utils.combine_imgs import create_comparison_image
from datetime import datetime
import torch

torch.classes.__path__ = []
def get_custom_css():
    """Return custom CSS for the Streamlit app"""
    return """
    <style>
    /* Main container styling */
    .main {
        padding-top: 2rem;
    }
     .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    /* Upload section styling */
    .upload-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem -1rem 2rem -1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    /* Workflow step cards */
    .workflow-step {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    
    .workflow-step:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .workflow-step strong {
        color: #2c3e50;
        font-size: 1.2rem;
    }
    
    /* File uploader styling */
    div[data-testid="stFileUploader"] {
        background: #f8f9fa;
        border: 2px dashed #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        transition: all 0.3s;
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: #4CAF50;
        background: #f1f8f4;
    }
    
    /* Button styling */
    div[data-testid="stButton"] > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Results section */
    .results-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    /* Spinner styling */
    div[data-testid="stSpinner"] {
        text-align: center;
    }
    
    /* Headers */
    h1 {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    h2, h3 {
        color: #34495e;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }
    </style>
    """

def create_result_card(conf_text, icon, color, score):
    """Create a styled result card"""
    conf_percent = f"{score * 100:.1f}"
    
    result_html = f"""
    <div style="
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 1rem;
    ">
        <div style="
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background-color: {color};
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 48px;
            font-weight: bold;
            margin: 0 auto 1.5rem;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        ">{icon}</div>
        
        <h2 style="
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: {color};
            font-weight: 700;
        ">{conf_text}</h2>
        
        <p style="
            font-size: 1.3rem;
            color: #5a6c7d;
            margin-bottom: 1.5rem;
        ">
            with <span style="color: {color}; font-weight: bold;">{conf_percent}%</span> confidence
        </p>
        
        <div style="
            background-color: rgba(0,0,0,0.05);
            border-radius: 10px;
            padding: 0.5rem;
            margin-top: 1rem;
        ">
            <div style="
                height: 20px;
                background-color: #e9ecef;
                border-radius: 10px;
                overflow: hidden;
            ">
                <div style="
                    width: {conf_percent}%;
                    height: 100%;
                    background-color: {color};
                    transition: width 1s ease-in-out;
                "></div>
            </div>
        </div>
        
        <p style="
            margin-top: 1.5rem;
            font-size: 0.9rem;
            color: #8b9dc3;
        ">
            Analysis completed on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
        </p>
    </div>
    """
    
    st.html(result_html)
        
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🔍 Signature Forgery Detection</h1>
    <p>Analyze a signature against a known signature to detect forgery.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap='medium')

with col1:
    st.markdown("""
    <div class="workflow-step">
        <strong>Step 1: Upload Known Signature</strong>
    </div>
    """, unsafe_allow_html=True)
    
    img1_upload = st.file_uploader(
        label="Upload genuine signature", 
        type=["jpg", "jpeg", "png"], 
        key='img1',
        help="Upload a clear image of the known genuine signature"
    )
    
    if img1_upload:
        st.success("✓ Genuine signature uploaded")

with col2:
    st.markdown("""
    <div class="workflow-step">
        <strong>Step 2: Upload Questioned Signature</strong>
    </div>
    """, unsafe_allow_html=True)
    
    img2_upload = st.file_uploader(
        label="Upload questioned signature", 
        type=["jpg", "jpeg", "png"], 
        key='img2',
        help="Upload the signature you want to verify"
    )
    
    if img2_upload:
        st.success("✓ Questioned signature uploaded")

    
# Submit button
img_sub = st.button("🔍 Verify Signatures", type='primary', use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
if img_sub:
    if img1_upload and img2_upload:
        # Create results container
        st.html('<div class="results-container">')
        
        # Create columns for results
        result_col1, result_col2 = st.columns([1, 1], gap='large')
        
        with result_col1:
            with st.spinner("🔄 Analyzing signatures..."):
                try:
                    # Load model
                    model = pipeline("image-classification", 'aevalone/vit-base-patch16-224-finetuned-forgery')
                    
                    # Create comparison image
                    combined_img = create_comparison_image(img1_upload, img2_upload)
                    
                    st.subheader("📊 Signature Comparison")
                    st.image(combined_img, caption="Side-by-side signature comparison",  use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.stop()
        
        with result_col2:
            try:
                # Get model results
                results = model(combined_img)
                
                # Process results
                gscore = 0
                fscore = 0
                
                for r in results:
                    if r.get('label') == 'genuine':
                        gscore = r.get('score', 0)
                    elif r.get('label') == 'forgery':
                        fscore = r.get('score', 0)
                
                # Determine final result
                if gscore > fscore:
                    final_result = "Genuine"
                    final_score = gscore
                    result_color = "#28a745"
                    icon = "✓"
                    conf_text = "GENUINE"
                else:
                    final_result = "Forged"
                    final_score = fscore
                    result_color = "#dc3545"
                    icon = "✗"
                    conf_text = "FORGERY"
                
                # Display results
                st.subheader("🎯 Verification Results")
                
                # Create result card
                create_result_card(conf_text, icon, result_color, final_score)
                
                # Additional details
                if final_score > 0.8:
                    st.success("High confidence - The model is very certain about this prediction")
                elif final_score > 0.6:
                    st.warning("Medium confidence - The model has reasonable certainty")
                else:
                    st.info("Low confidence - Consider additional analysis or expert review")
                
                # Show balloons for genuine signatures
                if final_result == "Genuine":
                    st.balloons()
                    
            except Exception as e:
                st.error(f"❌ Error processing results: {str(e)}")
        
        st.html('</div>')
        
    else:
        st.warning("⚠️ Please upload both signature images before verification")