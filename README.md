# L'Alchimie Numérique (Digital Alchemy)
> A poetic image transformation pipeline combining AI vision and generation

## Overview
L'Alchimie Numérique is an artistic project that transforms images through a three-stage process, combining AI vision, language processing, and image generation. The project name reflects its nature of digital transformation, much like the ancient art of alchemy.

## Process
The transformation occurs in three distinct acts:

### 1. Image Analysis (Premier acte)
- Uses OpenAI's vision capabilities through LLM CLI
- Converts image content into textual descriptions
- Processes input images and generates detailed descriptions

### 2. Prompt Engineering (Deuxième acte)
- Transforms image descriptions into creative prompts
- Utilizes Replicate's AI models for image generation
- Creates a bridge between textual and visual representations

### 3. Image Generation (Troisième acte)
- Powered by Python and Replicate API
- Generates new images based on the transformed prompts
- Creates unique visual interpretations

## Technical Components

### Scripts
1. `daily.sh`: Shell script for processing input images
   - Handles input validation
   - Creates necessary output directories
   - Processes images using LLM CLI

2. `gen_img.py`: Python script for image generation
   - Integrates with Replicate API
   - Includes robust error handling and logging
   - Processes prompts from XML-formatted files

### File Structure