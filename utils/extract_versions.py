import re
import fitz
import difflib
import streamlit as st

def extract_pdf_versions(pdf_data):
    """Extract all PDF versions from incremental updates"""
    if hasattr(pdf_data, 'read'):
        pdf_data = pdf_data.read()
        
    startxref_positions = [m.start() for m in re.finditer(b'startxref', pdf_data)]
    
    if len(startxref_positions) <= 1:
        print("No incremental updates detected in this PDF.")
        return []
    
    print(f"Found {len(startxref_positions)} potential versions")
    
    # Find EOF positions for each version
    eof_positions = []
    for pos in startxref_positions:
        eof_pos = pdf_data.find(b'%%EOF', pos)
        if eof_pos != -1:
            eof_positions.append(eof_pos + 5)  # +5 to include %%EOF
    
    # Extract version data (each version is cumulative)
    versions = []
    for i, eof_pos in enumerate(eof_positions):
        version_data = pdf_data[:eof_pos]
        versions.append(version_data)
    
    return versions

def extract_text_from_pdf_data(pdf_data):
    """Extract text from PDF data without saving to file"""
    try:
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page_num in range(len(doc)):
            text += doc[page_num].get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
 
def compare_pdf_versions(versions):
    """Compare consecutive PDF versions and return differences"""
    if len(versions) < 2:
        print("Need at least two versions to compare")
        return []

    # Extract text from all versions
    version_texts = []
    for i, version_data in enumerate(versions):
        text = extract_text_from_pdf_data(version_data)
        version_texts.append(text)
        print(f"Version {i+1}: {len(text)} characters extracted")

    return version_texts

def generate_version_diffs(version_texts):
    """Generate diffs between consecutive versions"""
    diffs = []
    
    for i in range(len(version_texts) - 1):
        prev_text = version_texts[i]
        curr_text = version_texts[i + 1]
        
        print(f"\nComparing Version {i+1} with Version {i+2}:")
        
        # Check for empty or failed extractions
        if not prev_text.strip() or not curr_text.strip():
            print(f"  Skipping comparison - empty text for Version {i+1} or Version {i+2}")
            diffs.append(None)
            continue
        
        # Basic difference check
        if prev_text == curr_text:
            print("  No text differences detected")
            diffs.append([])
            continue
        
        # Generate unified diff
        diff_lines = list(difflib.unified_diff(
            prev_text.splitlines(),
            curr_text.splitlines(),
            fromfile=f'Version {i+1}',
            tofile=f'Version {i+2}',
            lineterm=''
        ))
        
        # Count changes
        additions = len([line for line in diff_lines if line.startswith('+')])
        removals = len([line for line in diff_lines if line.startswith('-')])
        print(f"  Changes: {additions} additions, {removals} removals")
        
        diffs.append(diff_lines)
    
    return diffs

def display_diff_summary(diffs):
    """Display a summary of differences without complex data structures"""
    if not diffs:
        st.write("No diffs to display")
        return
    
    for i, diff in enumerate(diffs):
        st.subheader(f"Version {i+1} → Version {i+2}")
        
        if diff is None:
            st.write("⚠️ Comparison skipped (empty text)")
        elif not diff:
            st.write("✅ No differences detected")
        else:
            # Count changes
            additions = len([line for line in diff if line.startswith('+')])
            removals = len([line for line in diff if line.startswith('-')])
            
            st.write(f"📊 **Changes:** {additions} additions, {removals} removals")

            st.code('\n'.join(diff), language='diff')

                    
def analyze_pdf_versions(pdf_data):
    """Main function to analyze PDF versions without saving files"""
    # Extract all versions
    versions = extract_pdf_versions(pdf_data)
    if not versions:
        return None
    
    # Extract text from all versions
    version_texts = compare_pdf_versions(versions)
    
    # Generate diffs between consecutive versions
    diffs = generate_version_diffs(version_texts)
    
    return {
        'versions': versions,
        'texts': version_texts,
        'diffs': diffs
    }