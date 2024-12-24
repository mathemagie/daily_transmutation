#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide an input image file"
    echo "Usage: $0 <input_image_file>"
    exit 1
fi

# Create output directory if it doesn't exist
if [ ! -d "output" ]; then
    mkdir output
    echo "Created output directory"
fi


# Store the input file path
INPUT_FILE="$1"

# Check if the file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' does not exist"
    exit 1
fi

# Create output directory if it doesn't exist
echo "describing image..."
llm < promp.txt -a $INPUT_FILE > output/output.txt
echo "generating image..."
python gen_img.py output/output.txt
echo "image generated"
