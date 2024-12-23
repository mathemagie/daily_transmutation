import replicate
import requests
import logging
import datetime
# Add logging configuration at the top
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_generator.log'),
        logging.StreamHandler()  # This will print to console as well
    ]
)
logger = logging.getLogger(__name__)

def read_prompt_from_file(filename="output.txt"):
    """
    Read and extract prompt from file between <prompt> tags
    Returns the prompt text or None if there's an error
    """
    try:
        logger.info(f"Reading prompt from file: {filename}")
        # Read the prompt file with explicit encoding
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        # Extract the prompt text between tags
        start_tag = "<prompt>"
        end_tag = "</prompt>"
        start_index = content.find(start_tag) + len(start_tag)
        end_index = content.find(end_tag)
        
        if start_index == -1 or end_index == -1:
            logger.error("Prompt tags not found in file")
            raise ValueError("Prompt tags not found in file")
            
        prompt = content[start_index:end_index].strip()
        logger.info(f"Successfully extracted prompt: {prompt[:50]}...")
        return prompt
    
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found")
        return None
    except Exception as e:
        logger.error(f"Error reading prompt: {str(e)}")
        return None

def generate_image(prompt):
    """
    Generate image using Replicate API
    Returns the image URL or None if there's an error
    """
    try:
        logger.info("Generating image with Replicate API")
        result = replicate.run(
            "black-forest-labs/flux-1.1-pro-ultra",
            input={
                "raw": False,
                "prompt": prompt,
                "aspect_ratio": "3:2",
                "output_format": "jpg",
                "safety_tolerance": 2,
                "image_prompt_strength": 0.1,
            },
        )
        logger.info(f"Successfully generated image URL: {result}")
        return result
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return None

def download_image(img_url, filename="generated_image.jpg"):
    """
    Download image from URL and save it locally
    Returns True if successful, False otherwise
    """
    try:
        logger.info(f"Downloading image from URL: {img_url}")
        # Add timeout to prevent hanging
        response = requests.get(img_url, timeout=30)
        response.raise_for_status()  # Raise exception for bad status codes

        # Save the image locally
        # Generate timestamp for unique filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.jpg"
        with open(filename, "wb") as f:
            f.write(response.content)
        logger.info(f"Image downloaded successfully and saved as '{filename}'")
        return True

    except requests.Timeout:
        logger.error("Request timed out while downloading image")
    except requests.RequestException as e:
        logger.error(f"Error downloading image: {str(e)}")
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
    return False

def main():
    logger.info("Starting image generation process")
    # Read prompt from file
    prompt = read_prompt_from_file()
    if not prompt:
        return

    # Generate image
    img_url = generate_image(prompt)
    if not img_url:
        return

    # Download and save image
    download_image(img_url)

if __name__ == "__main__":
    main()
