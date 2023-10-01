
import os
from utils import is_valid_url
from pydantic import BaseModel, field_validator


class CFGGeneral(BaseModel):
    root_path: str
    whisper_url: str

    @field_validator('root_path')
    def validate_root_path(cls, path):
        # assert that the path exists
        assert os.path.exists(path), f'Invalid path: {path}'
        return path

    @field_validator('whisper_url')
    def validate_whisper_url(cls, url):
        # assert that the url is valid
        assert is_valid_url(url), f'Invalid url: {url}'
        return url

class CFGModel(BaseModel):
    model_name: str
    version: str
    download_path: str
    download_version: str
    size: str

class CFGWhisper(CFGModel):
    n_vocab: str
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

class CFGProgram(BaseModel):
    general: CFGGeneral
    whisper: CFGWhisper


