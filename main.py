import io
import requests

import speech_recognition as sr 
from fastapi import FastAPI, File, UploadFile , HTTPException

from fastapi.responses import HTMLResponse
import moviepy.editor as mp

app = FastAPI(
    title="convert video voice to text",
    description="upload the video and get the text in response file (duration of video is not more than 2 min)",
    version="1.0",
)


@app.get("/")
async def root():
    return "Welcome User !!"


@app.post("/uploadfile/")
async def upload_video_file(file: UploadFile = File(...)):
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