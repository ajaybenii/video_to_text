from typing import List

from fastapi import FastAPI, File, UploadFile , HTTPException
from fastapi.responses import HTMLResponse
import speech_recognition as sr 
import moviepy.editor as mp
import requests
import io
app = FastAPI(
    title="convert voice to text",
    description="upload the video and get the text in response file (duration of video is not more than 2 min)",
    version="1.0",
)


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:    # response = requests.get(URL)
        path = (file.filename)
        clip = mp.VideoFileClip(path) 
    
        clip.audio.write_audiofile(r"audio.wav")

        r = sr.Recognizer()

        audio = sr.AudioFile("audio.wav")

        with audio as source:
            audio_file = r.record(source)
        result = r.recognize_google(audio_file)

        # exporting the result 
        with open('recognized_text.txt',mode ='w') as file: 
            file.write("Recognized Speech:") 
            file.write("\n") 
            file.write(result) 
            # print(result)
            return {"text": result}
    except:
        raise HTTPException(status_code=406, detail="Please upload a video clip duration is less than 2 minutes and size will be not more than 10 mb ")