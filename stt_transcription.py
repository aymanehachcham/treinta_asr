


from google.cloud import speech
import logging
import timeit

def transcribe_file(gc_uri: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file."""
    logging.basicConfig(level=logging.INFO)
    client = speech.SpeechClient.from_service_account_file('keys.json')
    audio = speech.RecognitionAudio(uri=gc_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="es-CO",
        enable_automatic_punctuation=True,
    )

    start = timeit.default_timer()
    operation = client.long_running_recognize(config=config, audio=audio)
    logging.info("Waiting for the Cloud STT api to retrieve the transcript...")
    response = operation.result(timeout=90)
    stop = timeit.default_timer()
    logging.info(f"Transcript retrieved in {stop - start} seconds\n\n")

    transcript_builder = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        transcript_builder.append(f"{result.alternatives[0].transcript}")
        # transcript_builder.append(f"\nConfidence: {result.alternatives[0].confidence}")

    transcript = "".join(transcript_builder)


    return transcript




if __name__ == '__main__':
    print(transcribe_file('gs://asr_treinta_bucket/audio_sample_2_2.wav'))