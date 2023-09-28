
import os
import requests
from tqdm import tqdm
from subprocess import Popen
from pathlib import Path
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceModel(BaseModel):
    name: str
    path: str

class ModelConfig:

    @classmethod
    def _get_model_dir(cls):
        return Path(os.path.expanduser('~')) / ".asr" / "models"

    @classmethod
    def _save_pretrained_model(cls) -> bool:
        pass

    @classmethod
    def download_whisper_model(
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
    def download_whisper(
            cls,
            model_name: str = 'small.en',
    ):
        """
        Download whisper model from huggingface, following a specific routine.
        :param model_name:
        :return: None
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
            with open(f'ggml-{model_name}.bin', 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

        logging.info(f'Model {model_name} downloaded successfully. \n')
        return



if __name__ == '__main__':
    ModelConfig.download_whisper(model_name='tiny.en')