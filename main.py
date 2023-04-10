import pdfkit
import whisper
from pytube import YouTube
import moviepy.editor as mp


##take the url and convert to mp3 save it to the pc
def videotomp3():
    file_url = input("Enter the Url of the video")
    #https://www.youtube.com/watch?v=5JK7vjVaIvo
    path_of_file_name = YouTube(file_url).streams.first().download()
    print(type(path_of_file_name))
    clip = mp.VideoFileClip(path_of_file_name)
    clip.audio.write_audiofile(path_of_file_name+".mp3")
    transcript(path_of_file_name)
#take the mp3 file and then transcribe it

import json

def transcript(audio):
    model = whisper.load_model("base")
    result = model.transcribe(audio)
    print("Converting to pdf")
    ##Append the converted text to PDF file and save it
    pdfkit.from_string(result["text"], audio+".pdf")

if __name__ == '__main__':
    videotomp3()

