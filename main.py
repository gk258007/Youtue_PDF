import pdfkit
import whisper
from pytube import YouTube
import moviepy.editor as mp
import PyPDF2
import openai
import os
##take the url and convert to mp3 save it to the pc

openai.api_key = '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'

def videotomp3():
    file_url = input("Enter the url of the youtube")
    path_of_file_name = YouTube(file_url,use_oauth=True, allow_oauth_cache=True).streams.first().download()
    clip = mp.VideoFileClip(path_of_file_name)
    # path_of_file_name = path_of_file_name.replace(" ","")
    print(path_of_file_name)
    clip.audio.write_audiofile(path_of_file_name+".mp3")
    transcript(path_of_file_name)
#take the mp3 file and then transcribe it


def summarize(file):
    pdf_summary_text = ""
    pdf_path = file
    print(file)
    pdf_file = open(pdf_path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text().lower()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                        {"role": "system", "content": "You are a helpful research assistant."},
                        {"role": "user", "content": f"Summarize this: {page_text}"},
                            ],
                                )
        page_summary = response["choices"][0]["message"]["content"]
        pdf_summary_text+=page_summary + "\n"
        pdf_summary_file = pdf_path.replace(os.path.splitext(pdf_path)[1], "_summary.txt")
        with open(pdf_summary_file, "w+") as file:
             file.write(pdf_summary_text)
    pdf_file.close()

    with open(pdf_summary_file,"r") as file:
        print(file.read())

def transcript(audio):
    model = whisper.load_model("base")
    result = model.transcribe(audio)
    print(result)
    print("Converting to pdf")
    ##Append the converted text to PDF file and save it
    audio=audio.replace(" ","")
    pdfkit.from_string(result["text"], audio+".pdf")
    file = audio+".pdf"
    print(file)
    summarize(file)

if __name__ == '__main__':
    videotomp3()
    #summarize();
    ##transcript('/Volumes/T7/backUp/coding/rock/py_yt_openai/audio_sample.mp3')

