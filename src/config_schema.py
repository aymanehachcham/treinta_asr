

from utils import is_valid_url
from typing import List
from pydantic import BaseModel, field_validator
import toml


class CFGGeneral(BaseModel):
    root_path: str
    whisper_url: str

    @field_validator('whisper_url')
    def validate_whisper_url(cls, url):
        # assert that the url is valid
        assert is_valid_url(url), f'Invalid url: {url}'
        return url

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

class Whisper(BaseModel):
    name: str
    version: str
    download_path: str
    checksum: str
    size: str
    available_models: List[str]
    config: CFGWhisper

class CFGModel(BaseModel):
    whisper: Whisper

class CFGProgram(BaseModel):
    general: CFGGeneral
    models: CFGModel



