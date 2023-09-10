
from pydub import AudioSegment

def convert_to_linear (audio_file: str, output_path: str) -> AudioSegment:
    """Converts an audio file to linear16 format"""
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio = audio.set_sample_width(2)
    audio.export(output_path, format='wav')


if __name__ == '__main__':
    convert_to_linear('audio_sample_2.wav', 'audio_sample_2_2.wav')