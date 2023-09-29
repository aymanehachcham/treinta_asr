
import os
import requests
from tqdm import tqdm
from subprocess import Popen
from pathlib import Path
import logging
from whispercpp import Whisper
import toml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_WHISPER_AVAILABLE_MODELS = [
    "tiny.en",
    "tiny",
    "tiny-q5_1",
    "tiny.en-q5_1",
    "base.en",
    "base",
    "base-q5_1",
    "base.en-q5_1",
    "small.en",
    "small.en-tdrz",
    "small",
    "small-q5_1",
    "small.en-q5_1",
    "medium",
    "medium.en",
    "medium-q5_0",
    "medium.en-q5_0",
    "large-v1",
    "large",
    "large-q5_0",
]

class ModelConfig:

    @classmethod
    def _get_model_dir(cls):
        return Path(os.path.expanduser('~')) / ".asr" / "models"

    @classmethod
    def _save_pretrained_model(cls) -> bool:
        pass

    @classmethod
    def _download_whisper_model_sh(
            cls,
            model_name: str = 'small.en',
    ) -> None:
        if not os.path.exists(cls._get_model_dir()):
            os.makedirs(cls._get_model_dir())
        print(os.getcwd())
        Popen(
            ['sh', './scripts/download_whisper.sh', model_name, str(cls._get_model_dir())],
        ).wait()

    @classmethod
    def _download_whisper_model(
            cls,
            model_name: str,
    ):
        """
        Download whisper model from huggingface, following a specific routine.
        :param model_name: The name of the model
        :return: Optional[str] The name of the model if it was downloaded successfully, None otherwise.
        """
        full_model_path = os.path.join(cls._get_model_dir(), f'ggml-{model_name}.bin')
        url = 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml'

        if not os.path.exists(cls._get_model_dir()):
            os.makedirs(cls._get_model_dir())

        if os.path.exists(full_model_path):
            logging.info(f'Model {model_name} already exists. Skipping download \n')
            return

        logging.info(f'Downloading model {model_name} from {url} \n')
        try:
            res = requests.get(f'{url}-{model_name}.bin', stream=True)
            res.raise_for_status()
        except requests.RequestException as e:
            logging.error(f'Error while downloading model {model_name} from {url} \n')
            logging.error(e)
            return

        total_size = int(res.headers.get('content-length', 0))
        with tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
            with open(full_model_path, 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

        logging.info(f'Model {model_name} downloaded successfully. \n')
        return

    @classmethod
    def load_pretrained_whisper(
            cls,
            model_name: str = 'small.en',
    ) -> Whisper:
        """
        Load a pretrained whisper model from huggingface.
        :param config: The model configuration.
        :return: A Speech2Transcription object.
        """
        if model_name not in _WHISPER_AVAILABLE_MODELS:
            raise ValueError(f'Model {model_name} not available. Available models are: {_WHISPER_AVAILABLE_MODELS}')

        cls._download_whisper_model(model_name)
        try:
            full_path = os.path.join(cls._get_model_dir(), f'ggml-{model_name}.bin')
        except FileNotFoundError:
            logging.error(f'Model {model_name} not found. \n')
            return

        whisper_config = toml.load('../config/whisper_config.toml')
        return Whisper.from_params(model_name=full_path, params=whisper_config['init_config_defaults'])







if __name__ == '__main__':
    model = ModelConfig.load_pretrained_whisper('tiny.en')