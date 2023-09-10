

import openai
import os
from stt_transcription import transcribe_file
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_API_KEY')

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "system",
            "content": "You are an assistant that provides information about a transcript audio file."
            "The idea is that based on the prompt given, try to explain the situation of what is being said in the transcript."
            "The transcript is given in colombian spanish."
        },
        {"role": "user", "content": f"This is the given transcript: {transcribe_file('gs://asr_treinta_bucket/audio_sample_2_2.wav')}"},
    ]
)

if __name__ == '__main__':
    print(completion.choices[0]['message']['content'])


