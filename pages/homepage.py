import streamlit as st



# Custom CSS for styling
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .feature-card {
        background: white;
        padding: 30px;
        color: black;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        height: 100%;
    }
    
    .icon-header {
        font-size: 3rem;
        margin-bottom: 20px;
    }
    
    .workflow-step {
        background: #f8f9fa;
        color: black;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1>🔍 Document Forensics Suite</h1>
    <h3>Advanced AI-Powered Document Authentication & Signature Analysis</h3>
    <p>Detect manipulations, verify signatures, and ensure document integrity with cutting-edge machine learning technology</p>
</div>
""", unsafe_allow_html=True)

# Main features section
st.markdown("## 🚀 Core Features")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-header">🔍</div>
        <h3>Document Manipulation Detection</h3>
        <p>Utilize Error Level Analysis (ELA) to identify altered areas in PDF documents. Our advanced algorithms detect:</p>
        <ul>
            <li>Digital tampering and modifications</li>
            <li>Content insertion or deletion</li>
            <li>Image compression inconsistencies</li>
            <li>Version tracking and changes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-header">✍️</div>
        <h3>Signature Detection & Extraction</h3>
        <p>Automatically locate and extract signatures from documents using YOLO-based object detection:</p>
        <ul>
            <li>Multi-page PDF signature detection</li>
            <li>Automatic signature cropping</li>
            <li>Batch processing capabilities</li>
            <li>Export individual signatures</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-header">🔐</div>
        <h3>Signature Verification</h3>
        <p>Compare signatures to determine authenticity using deep learning classification:</p>
        <ul>
            <li>Genuine vs. forged classification</li>
            <li>Confidence scoring</li>
            <li>Side-by-side comparison</li>
            <li>Expert-level accuracy</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# How it works section
st.markdown("## 📋 How to Use the System")

workflow_col1, workflow_col2 = st.columns([1, 2], gap="large")

with workflow_col1:
    st.markdown("""
    ### Quick Start Workflow
    
    <div class="workflow-step">
        <strong>Step 1:</strong> Choose your analysis type from the sidebar navigation
    </div>
    
    <div class="workflow-step">
        <strong>Step 2:</strong> Upload your PDF document or signature images
    </div>
    
    <div class="workflow-step">
        <strong>Step 3:</strong> Click submit and wait for AI analysis
    </div>
    
    <div class="workflow-step">
        <strong>Step 4:</strong> Review results and download reports
    </div>
    """, unsafe_allow_html=True)

with workflow_col2:
    st.markdown("""
    ### 🎯 Use Cases
    
    **Legal & Forensic Professionals:**
    - Document authenticity verification
    - Evidence analysis for court proceedings
    - Contract and agreement validation
    
    **Financial Institutions:**
    - Signature verification for transactions
    - Document fraud prevention
    - Compliance and audit support
    
    **Corporate Security:**
    - Internal document integrity checks
    - Employee verification processes
    - Intellectual property protection
    """)

st.markdown("---")

# Technical specifications
tech_col1, tech_col2, tech_col3 = st.columns(3, gap="large")

with tech_col1:
    st.markdown("""
    ### 🔧 Technical Capabilities
    
    **Supported Formats:**
    - PDF documents (multi-page)  
    - Image formats: JPG, JPEG, PNG
    - High DPI processing (up to 300 DPI)
    
    **Analysis Methods:**
    - Error Level Analysis (ELA)
    - YOLO object detection
    - Deep learning classification
    - Computer vision preprocessing
    """)

with tech_col2:
    st.markdown("""
    ### 🚀 AI Infrastructure
    
    **Model Development:**
    - Built with HP AI Studio
    - Trained on NVIDIA GPU clusters
    - Experiment tracking via MLFlow
    - Enterprise-grade model management
    
    **Deployment:**
    - ONNX optimized models
    - Hardware-accelerated inference
    - Scalable architecture
    """)

with tech_col3:
    st.markdown("""
    ### 📊 Performance Metrics
    
    **Detection Accuracy:**
    - Signature detection: >95% precision
    - Forgery classification: >90% accuracy
    - Manipulation detection: Advanced ELA algorithms
    
    **Processing Speed:**
    - Real-time analysis
    - Batch processing support
    - GPU-optimized inference
    """)

st.markdown("---")

# Navigation guide
st.markdown("## 🧭 Navigation Guide")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.info("""
    **📄 Signature Detection**
    
    Upload PDF documents to automatically detect and extract all signatures. Perfect for processing contracts, legal documents, and forms.
    """)

with nav_col2:
    st.info("""
    **🔍 Document Analysis**
    
    Analyze PDFs for digital manipulations and tampering. Uses advanced ELA techniques to highlight suspicious areas.
    """)

with nav_col3:
    st.info("""
    **🔐 Signature Verification**
    
    Compare two signature images to determine if they're genuine or forged. Get confidence scores and detailed analysis.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 20px;">
    <p>🛡️ Powered by advanced AI models developed with HP AI Studio, NVIDIA GPUs & MLFlow</p>
    <p>Enterprise-grade machine learning infrastructure for professional document forensics</p>
    <p>For technical support or questions, please refer to the documentation</p>
</div>
""", unsafe_allow_html=True)