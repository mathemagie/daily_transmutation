import replicate
import requests
import logging
import datetime
import sys
import traceback

# Configure logging
LOG_FILE = "gen_img.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler(LOG_FILE),  # Output to file
    ],
)
logger = logging.getLogger(__name__)


def read_prompt_from_file(filename="output.txt"):
    """
    Read and extract prompt from file between <prompt> tags
    Returns the prompt text or None if there's an error
    """
    try:
        logger.info(f"Reading prompt from file: {filename}")
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

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
        logger.error(f"File not found: {filename}")
        return None
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.error(traceback.format_exc())
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
    except replicate.ReplicateError as re:
        logger.error(f"Replicate API error: {re}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.error(traceback.format_exc())
        return None


def download_image(img_url, filename="generated_image.jpg"):
    """
    Download image from URL and save it locally
    Returns True if successful, False otherwise
    """
    try:
        logger.info(f"Downloading image from URL: {img_url}")
        response = requests.get(img_url, timeout=30)
        response.raise_for_status()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.jpg"
        with open(filename, "wb") as f:
            f.write(response.content)
        logger.info(f"Image downloaded successfully and saved as '{filename}'")
        return True

    except requests.Timeout:
        logger.error("Request timed out while downloading image")
        return False
    except requests.RequestException as re:
        logger.error(f"Request error: {re}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.error(traceback.format_exc())
        return False


def main():
    logger.info("Starting image generation process")
    if len(sys.argv) != 2:
        logger.error("Usage: python gen_img.py <prompt_file>")
        sys.exit(1)

    file_prompt = sys.argv[1]
    prompt = read_prompt_from_file(file_prompt)
    if not prompt:
        logger.error("Failed to read prompt. Exiting.")
        sys.exit(1)

    img_url = generate_image(prompt)
    if not img_url:
        logger.error("Failed to generate image. Exiting.")
        sys.exit(1)

    if not download_image(img_url):
        logger.error("Failed to download image. Exiting.")
        sys.exit(1)

    logger.info("Image generation process completed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
