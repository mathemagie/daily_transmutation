import replicate
import requests

def read_prompt_from_file(filename="output.txt"):
    """
    Read and extract prompt from file between <prompt> tags
    Returns the prompt text or None if there's an error
    """
    try:
        # Read the prompt file with explicit encoding
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        # Extract the prompt text between tags
        start_tag = "<prompt>"
        end_tag = "</prompt>"
        start_index = content.find(start_tag) + len(start_tag)
        end_index = content.find(end_tag)
        
        if start_index == -1 or end_index == -1:
            raise ValueError("Prompt tags not found in file")
            
        return content[start_index:end_index].strip()
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error reading prompt: {str(e)}")
        return None

def generate_image(prompt):
    """
    Generate image using Replicate API
    Returns the image URL or None if there's an error
    """
    try:
        return replicate.run(
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
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def download_image(img_url, filename="generated_image.jpg"):
    """
    Download image from URL and save it locally
    Returns True if successful, False otherwise
    """
    try:
        # Add timeout to prevent hanging
        response = requests.get(img_url, timeout=30)
        response.raise_for_status()  # Raise exception for bad status codes

        # Save the image locally
        with open(filename, "wb") as f:
            f.write(response.content)
        print("Image downloaded successfully and saved as 'generated_image.jpg'")
        return True

    except requests.Timeout:
        print("Error: Request timed out while downloading image")
    except requests.RequestException as e:
        print(f"Error downloading image: {str(e)}")
    except Exception as e:
        print(f"Error saving image: {str(e)}")
    return False

def main():
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
