#!/bin/bash

# Set the source URL and model name
src="https://huggingface.co/TheBloke/Llama-2-13B-GGUF"
model="llama-2-13b.Q4_K_M.gguf"

# Download model
printf "Downloading model $model from '$src' ...\n"

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

printf "Done! Model '$model' saved as '$model'\n"
