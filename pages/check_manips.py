import streamlit as st

from shared_utils import analyze_pdf_versions, display_diff_summary, ModdedDocAnalyzer
import torch

torch.classes.__path__ = []

analyzer = ModdedDocAnalyzer()
    
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
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

st.markdown("""
<div class="main-header">
    <h1>🔍 PDF Manipulation Detector</h1>
    <p>Analyze PDF documents for potential modifications and version history</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.3, 0.7], gap='large')


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
                    st.markdown("## Detection Results")
                    st.markdown("""
                                  
                    <div class="workflow-step">
                        <strong>Image manipulations will show up as highlighted areas in the image if any exist. If no manipulations were found, no highlights will appear.</strong>
                    </div>

                    """, unsafe_allow_html=True)
                    st.divider()
                    st.image(result_img)
            with c2:
                result = analyze_pdf_versions(manip_uploader)
                with st.container(key='version-card'):
                    display_diff_summary(result.get('diffs'))