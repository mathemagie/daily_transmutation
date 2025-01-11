#!/bin/bash


set -euo pipefail

# Define constants
readonly OUTPUT_DIR="output"
readonly OUTPUT_FILE="${OUTPUT_DIR}/output.txt"
readonly PROMPT_FILE="prompt.xml"

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide an input image file"
    echo "Usage: $0 <input_image_file>"
    exit 1
fi

# Create output directory if it doesn't exist
if [ ! -d "${OUTPUT_DIR}" ]; then
    mkdir "${OUTPUT_DIR}"
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
echo "describing image with OPENAI API call with LLM CLI ..."
llm < ${PROMPT_FILE} -a $INPUT_FILE > ${OUTPUT_FILE}
echo "DONE : image described"
cat ${OUTPUT_FILE}
echo "generating image with black-forest-labs/flux-1.1-pro-ultra model ..."
python gen_img.py ${OUTPUT_FILE}
echo "DONE : image generated"