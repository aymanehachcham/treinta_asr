import tkinter as tk
from tkinter import simpledialog, messagebox
import pyaudio
import wave
from google.cloud import speech_v1
from google.cloud.speech_v1 import types
import os
import threading
import openai
import requests

# Initialize OpenAI
openai.api_key = 'YOUR_API_KEY_HERE'  # Replace with your actual API key

# Global vars
recording = False
stream = None
frames = []
client = speech_v1.SpeechClient()

p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

def update_state_label(state_text):
    state_label.config(text=state_text)
    root.update()

def start_record():
    global recording, stream, frames, p, FORMAT, CHANNELS, RATE, CHUNK
    update_state_label("Recording")
    recording = True
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

def threaded_start_record():
    record_thread = threading.Thread(target=start_record)
    record_thread.start()

def stop_record():
    global recording, stream, frames, p, FORMAT, CHANNELS, RATE, CHUNK
    recording = False
    stream.stop_stream()
    stream.close()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    update_state_label("Transcribing")
    transcription = transcribe_audio(WAVE_OUTPUT_FILENAME)
    
    update_state_label("Analyzing")
    gpt_response = send_to_openai_gpt(transcription, prompt_entry.get(), int(max_tokens_entry.get()))
    
    update_state_label("Available")
    update_response(transcription, gpt_response['choices'][0]['message']['content'].strip())

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=44100, language_code="en-US")
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript
    return "No transcription available."

# Bad request sender.
def send_to_openai_gpt(text, prompt, max_tokens):
    headers = {
        'Authorization': f'Bearer {openai.api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt + " " + text}
        ],
        "max_tokens": max_tokens
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data).json()
    return response

def update_response(user_text, assistant_text):
    gpt_output.insert(tk.END, "Client: ", 'client_tag')
    gpt_output.insert(tk.END, user_text + "\n", 'user_text_tag')
    transcription_box.insert(tk.END, user_text + "\n")
    gpt_output.insert(tk.END, "Assistant: ", 'assistant_tag')
    gpt_output.insert(tk.END, assistant_text + "\n", 'assistant_text_tag')

# GUI setup
root = tk.Tk()
root.title("Automatic Script")
root.geometry('800x600')

# Style configurations
btn_bg_color = "#a3c2fa"
btn_active_bg_color = "#748cbf"
bg_color = "#f4f6f7"
root.configure(bg=bg_color)

# Left frame for most of the content
left_frame = tk.Frame(root, bg=bg_color)
left_frame.pack(side=tk.LEFT, padx=20, pady=20)

# State Label above "Enter GPT-3 Prompt"
state_label = tk.Label(left_frame, text="Available", bg=bg_color, font=("Arial", 14))
state_label.pack(pady=10)

prompt_label = tk.Label(left_frame, text="Enter GPT-3 Prompt:", bg=bg_color)
prompt_label.pack(pady=10)

prompt_entry = tk.Entry(left_frame, width=60)
prompt_entry.pack(pady=10)

max_tokens_label = tk.Label(left_frame, text="Max Response Tokens:", bg=bg_color)
max_tokens_label.pack(pady=10)

max_tokens_entry = tk.Entry(left_frame, width=10)
max_tokens_entry.insert(0, "100")  # Default value of 100 tokens
max_tokens_entry.pack(pady=10)

btn_start = tk.Button(left_frame, text="Start Recording", command=threaded_start_record, bg=btn_bg_color, activebackground=btn_active_bg_color)
btn_start.pack(pady=20)

btn_stop = tk.Button(left_frame, text="Stop Recording", command=stop_record, bg=btn_bg_color, activebackground=btn_active_bg_color)
btn_stop.pack(pady=20)

transcription_label = tk.Label(left_frame, text="Transcription:", bg=bg_color)
transcription_label.pack(pady=10)

transcription_box = tk.Text(left_frame, height=5, width=40)
transcription_box.pack(pady=10, expand=True, fill=tk.BOTH)

# Right frame for GPT-3.5 Response
right_frame = tk.Frame(root, bg=bg_color)
right_frame.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

gpt_label = tk.Label(right_frame, text="GPT-3.5 Response:", bg=bg_color)
gpt_label.pack(pady=10)

gpt_output = tk.Text(right_frame, height=10, width=40)
gpt_output.pack(pady=10, expand=True, fill=tk.BOTH)

# Text tags for formatting
gpt_output.tag_configure('client_tag', foreground='red', font=('Arial', 10, 'bold'))
gpt_output.tag_configure('user_text_tag', foreground='red')
gpt_output.tag_configure('assistant_tag', foreground='blue', font=('Arial', 10, 'bold'))
gpt_output.tag_configure('assistant_text_tag', foreground='blue')

root.mainloop()