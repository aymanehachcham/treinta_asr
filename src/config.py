import os
import logging
import hashlib
import sys

import requests
import toml

from pathlib import Path
from typing import Literal
from whispercpp import Whisper
from tqdm import tqdm
from utils import get_model_size
from config_schema import CFGProgram, WhisperSerial

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelConfig:
    """
    Handles and correctly loads the models from the local disk.
    """

    @classmethod
    def __get_dir(cls, config: CFGProgram, dirname: Literal["models", "config"]):
        """
        Get the directory path for the models or config folder.
        :param config: The config object for the whole program
        :param dirname: Either 'models' or 'config'
        :return: directory path created
        """
        dir_path = Path(os.path.expanduser(config.general.root_path)) / dirname
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
        return dir_path

    @classmethod
    def _download_whisper_model(
        cls,
        model_name: str,
        config: CFGProgram,
    ):
        """
        Download whisper model from huggingface, following a specific routine.
        :param model_name: The name of the model
        :param config: The config object for the whole program
        :return: None
        """
        full_model_path = os.path.join(cls.__get_dir(config, "models"), f"ggml-{model_name}.bin")
        full_config_path = os.path.join(cls.__get_dir(config, "config"), f"ggml-{model_name}.toml")
        url = config.models.whisper.download_url
        available_models = dict(config.general.available_whisper_models)

        if model_name not in available_models.keys():
            logging.error(f"Model {model_name} not available. Available models are: {available_models.keys()} \n")
            return

        if os.path.exists(full_model_path):
            logging.info(f"Model {model_name} already exists. Skipping download \n")
            return

        logging.info(f"Downloading model {model_name} from {url} ... \n")
        try:
            res = requests.get(f"{url}-{model_name}.bin", stream=True)
            res.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Error while downloading model {model_name} from {url} \n")
            logging.error(e)
            return

        # Create a temp file to validate the checksum
        hasher = hashlib.sha1()
        temp_file_path = f"{full_model_path}.tmp"

        total_size = int(res.headers.get("content-length", 0))
        with tqdm(total=total_size, unit="iB", unit_scale=True) as pbar:
            with open(temp_file_path, "wb") as temp_file:
                for chunk in res.iter_content(chunk_size=8192):
                    if chunk:
                        hasher.update(chunk)
                        temp_file.write(chunk)
                        pbar.update(len(chunk))

        if hasher.hexdigest() != available_models[model_name]:
            logging.error("Checksum of the downloaded file does not match the expected value. \n")
            os.remove(temp_file_path)  # Remove the temp file
            return

        os.rename(temp_file_path, full_model_path)

        # Save the config file for the specific downloaded model
        with open(full_config_path, "w") as f:
            current_cfg = WhisperSerial(
                name=model_name,
                download_url=url,
                size=get_model_size(full_model_path),
                checksum=hasher.hexdigest(),
                config=config.models.whisper.config,
            ).model_dump()
            toml.dump(current_cfg, f)

        logging.info(f"Model {model_name} downloaded successfully. \n")

    @classmethod
    def _download_llama_model(
        cls,
        model_name: str,
        config: CFGProgram,
    ):
        pass

    @classmethod
    def _load_model(
        cls,
        model_name: str,
        config: CFGProgram,
    ) -> Whisper:
        """
        Load a whisper model from the local disk, with default config.
        :param model_name: name of the model to load
        :param config: The config object for the whole program
        :return: A Whisper instance from whispercpp
        """
        # Check if _download_whisper_model has been called before
        if not os.path.exists(os.path.join(cls.__get_dir(config, "models"), f"ggml-{model_name}.bin")):
            logging.info(f"Model {model_name} not found. Downloading it ... \n")
            cls._download_whisper_model(model_name, config)

        # Load the model config for the model_name
        full_config_path = os.path.join(cls.__get_dir(config, "config"), f"ggml-{model_name}.toml")
        full_model_path = os.path.join(cls.__get_dir(config, "models"), f"ggml-{model_name}.bin")
        if not os.path.exists(full_config_path):
            logging.error(f"No config file found for model {model_name}. \n")
            sys.exit(1)

        with open(full_config_path, "r") as f:
            model_config = toml.load(f)
            _model = Whisper.from_params(model_name=full_model_path, params=WhisperSerial(**model_config).config)
        return _model


if __name__ == "__main__":
    # How to use the config class
    with open("../config.toml", "r") as f:
        config = toml.load(f)

    cfg = CFGProgram(**config)
    print(dict(cfg.general.available_whisper_models))
    # model = ModelConfig._load_model("tiny.en", cfg)
