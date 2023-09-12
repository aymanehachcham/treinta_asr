

import openai
import os
from stt_transcription import STT
from dotenv import load_dotenv
import logging
from time import perf_counter

load_dotenv()
logger = logging.getLogger(__name__)


def engage_in_feedback():
    """
    This function is used to engage in feedback with the user.
    The user will be asked to provide feedback on the generated transcript.
    """
    openai.api_key = os.getenv('OPEN_AI_API_KEY')
    transcript = STT.openai_file_transcription(
        audio_file="audio_data/audio_sample_2.wav",
        prompt_guidance='Tienes que detectar quien habla en el audio.'
    )
    print(f"Transcript generated: {transcript}\n\n")
    logger.info('OPENAI API is running for feedback...\n\n')
    start_time = perf_counter()
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente que proporciona información sobre un archivo de audio transcrito."
                           "Basándote en la situación dada, detecta quién es el entrevistador y quién es el entrevistado."
                           "¿Cómo responderías a las preguntas del entrevistador como el entrevistado?"
                           "Formatea tus respuestas de una manera legible"
            },
            {"role": "user", "content": f"Esta es la transcripción: {transcript}"},

        ]
    )
    logger.info(f'Time taken by OPENAI GPT-3: {perf_counter() - start_time} seconds.')
    return completion.choices[0]['message']['content']


if __name__ == '__main__':
    print(engage_in_feedback())


