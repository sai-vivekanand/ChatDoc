import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
MAX_FILE_SIZE = 500 * 1024  # 500KB

def get_file_size_str(size_in_bytes: int) -> str:
    """Convert file size to human-readable string."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} bytes"
    else:
        return f"{size_in_bytes / 1024:.1f}KB"

# Page config
st.set_page_config(
    page_title="PDF Analysis with Mistral AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Analysis with Mistral AI")

# File size warning
st.warning(f"Maximum file size: {get_file_size_str(MAX_FILE_SIZE)}")

# File upload
uploaded_file = st.file_uploader("Upload a PDF", type=['pdf'])

if uploaded_file:
    # Display file information
    st.write("### File Details")
    st.info(f"""
    - Filename: {uploaded_file.name}
    - Size: {get_file_size_str(uploaded_file.size)}
    """)
    
    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error(f"File size exceeds maximum limit of {get_file_size_str(MAX_FILE_SIZE)}")
        st.stop()
    
    # Process the file
    with st.spinner("Processing PDF..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(f"{API_URL}/upload-pdf", files=files)
            
            if response.status_code == 200:
                data = response.json()
                extracted_text = data["extracted_text"]
                char_count = data["char_count"]
                
                st.success("PDF processed successfully!")
                
                # Main content area
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("### Extracted Text")
                    st.info(f"Total characters: {char_count}")
                    
                    # Show complete text
                    st.text_area(
                        "Complete text content",
                        extracted_text,
                        height=400
                    )
                    
                    # Download button
                    st.download_button(
                        "Download text",
                        extracted_text,
                        file_name=f"{uploaded_file.name}_text.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    # Summary section
                    st.write("### Generate Summary")
                    if st.button("Generate Summary"):
                        with st.spinner("Generating summary... This may take a moment."):
                            try:
                                response = requests.post(
                                    f"{API_URL}/summarize",
                                    json={"text_content": extracted_text},
                                    headers={'Content-Type': 'application/json'}
                                )
                                if response.status_code == 200:
                                    st.write("#### Summary")
                                    st.write(response.json()["summary"])
                                else:
                                    st.error("Error generating summary")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    
                    # Q&A section
                    st.write("### Ask Questions")
                    question = st.text_input("Enter your question about the PDF")
                    if question and st.button("Get Answer"):
                        with st.spinner("Finding answer... This may take a moment."):
                            try:
                                response = requests.post(
                                    f"{API_URL}/ask-question",
                                    json={
                                        "text_content": extracted_text,
                                        "question": question
                                    },
                                    headers={'Content-Type': 'application/json'}
                                )
                                if response.status_code == 200:
                                    st.write("#### Answer")
                                    st.write(response.json()["answer"])
                                else:
                                    st.error("Error processing question")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
            
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload a PDF file to begin.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>Upload PDFs up to 500KB for text extraction, summarization, and Q&A</small>
    </div>
    """,
    unsafe_allow_html=True
)