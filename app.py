import os
import streamlit as st
import pdfplumber
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_bytes):
    text = ""
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to handle image upload
def handle_image_upload(image_file):
    image = Image.open(image_file)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()

# Function to generate response using Gemini API
def generate_response(input_prompt):
    response = model.generate_content(input_prompt)
    return response.text

# Main function to run the Streamlit app
def main():
    st.title("Medical Report Analysis Chatbot")

    # Background image and style
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
    background-color: #f0f2f6;
    background-image: url("https://images.unsplash.com/photo-1588420343618-6141b3784bce?q=80&w=2012&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your medical report (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])

    if uploaded_file is not None:
        extracted_text = ""
        if uploaded_file.type == "application/pdf":
            # Handle PDF upload
            pdf_bytes = uploaded_file.read()
            extracted_text = extract_text_from_pdf(pdf_bytes)
        else:
            # Handle image upload
            image_bytes = handle_image_upload(uploaded_file)
            # Assuming you have a way to process the image bytes if necessary
            extracted_text = "Extracted text from image"

        st.text("Extracted Text:")
        st.write(extracted_text)

        st.text("Analyzing Report...")

        input_prompt = f"""
        You are an advanced AI with extensive training in medical analysis, healthcare diagnostics, and patient recommendations. Your task is to thoroughly analyze the provided medical report text and respond with detailed insights and guidance. Your analysis should be comprehensive, accurate, and clear.

        Medical Report Text:
        {extracted_text}

        Please provide the following information:

        1. **Analysis Result of the Report:**
            - Summarize the key findings from the report.
            - Interpret significant medical terms and their implications.

        2. **Potential Problems the Patient Might Face in the Near Future:**
            - Identify possible health risks or conditions based on the report findings.
            - Discuss the progression of any identified diseases or symptoms.

        3. **Assessment of the Report's Overall Quality:**
            - Evaluate whether the report indicates good or bad health.
            - Determine if the patient should be concerned about their health based on the findings.

        4. **Symptoms of Diseases That Might Occur:**
            - List potential diseases or conditions the patient might develop.
            - Describe the associated symptoms and early warning signs.

        5. **Recommendations for the Patient:**
            - Suggest lifestyle modifications or preventive measures.
            - Recommend medications, therapies, or treatments if applicable.
            - Advise on follow-up appointments or further medical evaluation.

        6. **Online Resources for Further Knowledge:**
            - Provide original website links to reputable websites for reliable medical information.
            - Suggest patient support groups or organizations for further assistance.

        Make sure your response is detailed, accurate, and tailored to the specific content of the medical report provided. Your goal is to offer the patient a thorough understanding of their health status and actionable advice to improve or maintain their well-being.
        """

        
        response = generate_response(input_prompt)
        st.subheader("Analysis Result")
        st.write(response)
    else:
        st.error("Please upload a medical report to continue.")

if __name__ == "__main__":
    main()
