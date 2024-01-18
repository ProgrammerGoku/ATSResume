from dotenv import load_dotenv

load_dotenv()


import streamlit as st
import os
from PIL import Image
import io
import base64
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input,pdf,content_prmpt):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input,pdf[0],content_prmpt])
    return response.text
def get_txt_response(input,content_prmpt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content([input,content_prmpt])
    return response.text

def input_pdf_setup(file):
    if file!=None:
        image=pdf2image.convert_from_bytes(file.read())
        first_pg=image[0]
        img_byte_arr=io.BytesIO()
        first_pg.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded!!")
    

st.set_page_config(page_title="ATS Resume expert")
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)
st.header("ATS for Resume")

input_text=st.text_area("Job Description",key="input")

file=st.file_uploader("Upload your resume in PDF",type=["pdf"])
footer = """
    <style>
        .footer {
            position:fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            font-size: 12px;
            color: #555;
        }
    </style>
    <div class="footer">
        <p>Made with <i class="fas fa-heart" style="color: #ee7c68;"></i> by Gokul Ram Subramani | Powered by <i class="fab fa-google" style="color: #151414;"></i>emini-Pro</p>
        <div class="social-media">
            <a href="https://www.linkedin.com/in/gokul-ram-s"><i class="fab fa-linkedin fa-3x"></i></a>
        </div>
    </div>
"""






if file!=None:
    st.write("PDF uploaded successfully")

bt1=st.button("Summarize my resume")
bt4=st.button("Summarize Job description")
bt3=st.button("Percentage Match for job")
bt2=st.button("How can I improve my resume?")
st.markdown(footer,unsafe_allow_html=True)



text1='''You are an experienced Resume reviewer, You have great knowledge in the field of Software Engineering,
        Data Science, Machine Learning, Artificial Intelligence and other growing technologies.
        Your task is to provide a brief summary of the provided resume and how it aligns well with the given job description.
        If it is not a standard resume mention that too.
        If you are the HR would you give this candidate oppurtunity?.
        '''

text2='''As an HR how would you suggest to improve the resume further, give some tips and tricks to get calls
        for the provided job description'''

text3='''As an ATS system provide how much percentage does the resume match with the given job description.
        Suggest some ways to improve the match percentage'''

text4='''Provide a brief summary of the provided job description and highlight the key qualifications required for the job'''
if bt1:
    if file!=None and input_text!="":
        pdf_content=input_pdf_setup(file)
        response=get_response(text1,pdf_content,input_text)
        st.subheader("Response:")
        st.write(response)
    elif(file==None):
        st.write("Please upload the resume")
    else:
        st.write("Please provide Job Description")
elif bt2:
    if file!=None and input_text!="":
        pdf_content=input_pdf_setup(file)
        response=get_response(text2,pdf_content,input_text)
        st.subheader("Response:")
        st.write(response)
    elif(file==None):
        st.write("Please upload the resume")
    else:
        st.write("Please provide Job Description")
elif bt3:
    if file!=None and input_text!="":
        pdf_content=input_pdf_setup(file)
        response=get_response(text3,pdf_content,input_text)
        st.subheader("Response:")
        st.write(response)
    elif(file==None):
        st.write("Please upload the resume")
    else:
        st.write("Please provide Job Description")

elif bt4:
    if input_text!="":
        response=get_txt_response(text4,input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.write("Please provide the Job Description")





