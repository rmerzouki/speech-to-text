import streamlit as st
from pytube import YouTube
import os
import sys
import time
import requests
from zipfile import ZipFile

st.markdown('# ✑ **Transcriber : Audio to Text App**')
bar = st.progress(0)

# Custom functions 

# 2. Retrieving audio file from YouTube video
def get_yt(URL): 
    video = YouTube(URL)
    yt = video.streams.get_audio_only()
    yt_file=yt.download()
    #st.write(str(yt_file))


    #st.info('2. Audio file has been retrieved from YouTube video')
    bar.progress(10)

# 2b. Uploading your audio file (second option)
def upload_file(uploaded_file):
    os.getcwd()
    with open(os.path.join(os.getcwd(),uploaded_file.name),"wb") as f:
        f.write(uploaded_file.getbuffer())
        #file_details = {"FileName":uploaded_file .name,"FileType":uploaded_file .type}
        #st.write(str(f))

    #st.info('2. Audio file has been uploaded')
    bar.progress(10)

# 3. Upload audio file to AssemblyAI

def transcribe_audio_file():

    current_dir = os.getcwd()

    for file in os.listdir(current_dir):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(current_dir, file)
            #print(mp4_file)
    filename = mp4_file
    bar.progress(20)

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))
    audio_url = response.json()['upload_url']
    #st.info('3. YouTube audio file has been uploaded to AssemblyAI')
    bar.progress(30)

    # 4. Transcribe uploaded audio file
    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
    "audio_url": audio_url
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    transcript_input_response = requests.post(endpoint, json=json, headers=headers)

    #st.info('4. Transcribing uploaded file')
    bar.progress(40)

    # 5. Extract transcript ID
    transcript_id = transcript_input_response.json()["id"]
    #st.info('5. Extract transcript ID')
    bar.progress(50)

    # 6. Retrieve transcription results
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }
    transcript_output_response = requests.get(endpoint, headers=headers)
    #st.info('6. Retrieve transcription results')
    bar.progress(60)
    st.warning('Transcription is processing ...')
    
    # Check if transcription is complete
    # from time import sleep

    while transcript_output_response.json()['status'] != 'completed':
        # sleep(120)
        # st.warning('Transcription is processing ...')
        transcript_output_response = requests.get(endpoint, headers=headers)
    
    bar.progress(100)
    st.warning('Transcription is processed.')
    st.balloons()

    # 7. Print transcribed text
    st.header('Output')
    st.success(transcript_output_response.json()["text"])

    # 8. Save transcribed text to file

    # Save as TXT file
    yt_txt = open('yt.txt', 'w')
    yt_txt.write(transcript_output_response.json()["text"])
    yt_txt.close()

    # Save as SRT file
    srt_endpoint = endpoint + "/srt"
    srt_response = requests.get(srt_endpoint, headers=headers)
    with open("yt.srt", "w") as _file:
        _file.write(srt_response.text)
    
    zip_file = ZipFile('transcription.zip', 'w')
    zip_file.write('yt.txt')
    zip_file.write('yt.srt')
    zip_file.close()
    
    # Remove mp4 file
    os.remove(filename)
    
#####

# The App

# 1. Read API_text from .env
api_key = st.secrets['api_key']

#st.info('1. API is read ...')

#st.warning('Awaiting URL input or uploaded audio file in the sidebar for transcription.')

# Sidebar
st.sidebar.header('Input parameter')


with st.sidebar.form(key='my_form'):
    URL = st.text_input('Enter URL of YouTube video:') #https://youtu.be/IUTGFQpKaPU (this is an example)
    uploaded_file = st.file_uploader("Upload your audio mp4 file:", type=["mp4"])
    submit_button = st.form_submit_button(label='Transcribe')

if (uploaded_file is None) and (str(URL)==''):
    st.warning('Awaiting URL input or uploaded audio file in the sidebar for transcription.')
    

# Run custom functions if file uploaded or URL is entered 
if submit_button:

    if (str(URL)!='') and (uploaded_file is not None):
            st.sidebar.warning('Only one option is possible!')
            raise Exception("You must provide a URL or an audio file, not both!")

    elif uploaded_file is not None:
        upload_file(uploaded_file)
        transcribe_audio_file()

    elif str(URL)!='':
        get_yt(URL)
        transcribe_audio_file()

    else:
        st.sidebar.warning('Please provide URL input or uploaded audio file! ')
        raise Exception("You must provide a URL or an audio file!")

    with open("transcription.zip", "rb") as zip_download:
        btn = st.download_button(
            label="Download ZIP",
            data=zip_download,
            file_name="transcription.zip",
            mime="application/zip"
        )