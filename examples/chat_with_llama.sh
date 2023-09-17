#!/bin/bash

# Change directory to the specified path
cd ../../llama.cpp

# Check if cd command was successful
if [ $? -ne 0 ]; then
    echo "Failed to change directory to ../../llama.cpp"
    exit 1
fi

# Execute the given command
./main -t 10 -m ../ASR_Treinta/models/llama-13b/llama-2-13b.Q4_K_M.gguf -c 512 -b 1024 -n 256 \
    --repeat_penalty 1.0 --color -i \
    -r "User:" -f prompts/chat-with-bob.txt


