
import re
import os
import hashlib
import numpy as np

def is_valid_url(url: str) -> bool:
    regex = re.compile(
        r'^https://huggingface\.co'  # The URL must start with 'https://huggingface.co'
        r'(/[a-zA-Z0-9@:%._\+~#=/{1,}\-]*)?'  # The rest of the URL can contain a path with common URL-allowed characters
        r'\Z'  # End of string
    )
    if not re.match(regex, url):
        return False

    return True

def get_model_size(file_path: str) -> str:
    size = os.path.getsize(file_path) / (1024 * 1024)
    size = np.round(size , 2)
    return str(size) + ' MB'

def compute_checksum(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

