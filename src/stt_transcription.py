
import os
from google.cloud import speech
import logging
import timeit
from dotenv import load_dotenv
import openai
from time import perf_counter

load_dotenv()

def google_file_transcription(
        gc_uri: str
) -> speech.RecognizeResponse:
    """
    Transcription of audio file in LINEAR16 format using Google Cloud Speech-to-Text API.
    Long format files are stored in the Google Cloud Storage bucket.

    :param gc_uri: The path to the audio file in the Google Cloud Storage bucket.
    :type gc_uri: str
    :return: The transcript of the audio file.
    """
    logging.basicConfig(level=logging.INFO)
    client = speech.SpeechClient.from_service_account_file('keys.json')
    audio = speech.RecognitionAudio(uri=gc_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="es-CO",
        enable_automatic_punctuation=True,
    )

    start_time = perf_counter()
    operation = client.long_running_recognize(config=config, audio=audio)
    logging.info("Waiting for the Cloud STT api to retrieve the transcript...")
    response = operation.result(timeout=90)
    logging.info(f"Transcript retrieved in {perf_counter() - start_time} seconds\n\n")

    transcript_builder = []
    for result in response.results:
        transcript_builder += [f"{result.alternatives[0].transcript}"]

    return "".join(transcript_builder)

def openai_file_transcription(
        model: str,
        audio_file: os.PathLike,
        prompt_guidance: str = None,
) -> str:
    """
    Transcription of audio file using the OPEN AI API.
    The model used here is whisper-1.

    :param model: Whisper-1 by default no oder model is available
    :type model: str
    :param audio_file: the audio file to be transcribed
    :type audio_file: os.PathLike
    :param prompt_guidance: A textual prompt to help the model understand the context of the audio file
    :type prompt_guidance: str
    :return: Transcript of the audio file
    """
    logging.basicConfig(level=logging.INFO)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    audio = open(audio_file, 'rb')
    start_time = perf_counter()
    transcript = openai.Audio.transcribe(
        model,
        audio,
        language="es",
        temperature=0.3,
        prompt=prompt_guidance,
    )
    logging.info(f'Time taken by OPENAI Whisper-1: {perf_counter() - start_time} seconds.\n\n')
    return '\n'.join(transcript['text'].split('.'))


if __name__ == '__main__':
    # print(google_file_transcription(os.getenv("GC_URI")))
    print(openai_file_transcription(
        "whisper-1",
        "audio_data/audio_sample_2.wav",
        prompt_guidance='Tienes que detectar quien habla en el audio.'))