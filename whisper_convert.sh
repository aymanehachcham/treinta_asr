#!/bin/bash

# Check if the input file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

input_file="$1"
output_directory="audio_data"
output_file="$output_directory/output_16.wav"

# Create audio_data directory if it doesn't exist
mkdir -p "$output_directory"

# Run ffmpeg command
ffmpeg -y -i "$input_file" -ar 16000 -ac 1 -c:a pcm_s16le "$output_file"

# Check if ffmpeg executed successfully
if [ $? -ne 0 ]; then
    echo "Error while preprocessing the audio."
    exit 1
fi

echo "Audio preprocessed successfully and saved to $output_file."
