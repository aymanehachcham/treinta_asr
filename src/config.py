
import os
from pathlib import Path

class ModelConfig:
    @classmethod
    def get_model_dir(cls):
        return Path(os.path.expanduser('~')) / ".asr" / "models"



if __name__ == '__main__':
    print(ModelConfig.get_model_dir())