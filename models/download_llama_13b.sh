#!/bin/bash

# Set the source URL and model name
src="https://huggingface.co/TheBloke/Llama-2-13B-GGUF/blob/main"
model="llama-2-13b.Q6_K.gguf"

# Get the directory path of this script
function get_script_path() {
    if [ -x "$(command -v realpath)" ]; then
        echo "$(dirname "$(realpath "$0")")"
    else
        local ret="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
        echo "$ret"
    fi
}

models_path="$(get_script_path)"

# Download model
printf "Downloading model $model from '$src' ...\n"

cd "$models_path"

if [ -f "$model" ]; then
    printf "Model $model already exists. Skipping download.\n"
    exit 0
fi

if [ -x "$(command -v wget)" ]; then
    wget --no-config --quiet --show-progress -O $model $src/$model
elif [ -x "$(command -v curl)" ]; then
    curl -L --output $model $src/$model
else
    printf "Either wget or curl is required to download models.\n"
    exit 1
fi

if [ $? -ne 0 ]; then
    printf "Failed to download model $model \n"
    printf "Please try again later or check the URL.\n"
    exit 1
fi

printf "Done! Model '$model' saved in '$models_path/$model'\n"
