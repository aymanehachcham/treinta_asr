

from utils import is_valid_url
from typing import List, Tuple
from pydantic import BaseModel, field_validator
import toml


class CFGGeneral(BaseModel):
    root_path: str
    available_whisper_models: List[Tuple[str, str]]

class CFGWhisper(BaseModel):
    n_vocab: int
    n_audio_ctx: int
    n_audio_state: int
    n_audio_head: int
    n_audio_layer: int
    n_text_ctx: int
    n_text_state: int
    n_text_head: int
    n_text_layer: int
    n_mels: int
    f16: int

class WhisperSerial(BaseModel):
    name: str
    download_url: str
    size: str
    checksum: str
    config: CFGWhisper

    @field_validator('download_url')
    def validate_whisper_url(cls, url):
        # assert that the url is valid
        assert is_valid_url(url), f'Invalid url: {url}'
        return url

class CFGModel(BaseModel):
    whisper: WhisperSerial

class CFGProgram(BaseModel):
    general: CFGGeneral
    models: CFGModel

if __name__ == '__main__':
    with open('../config.toml', 'r') as f:
        config = toml.load(f)




