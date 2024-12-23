import replicate
import requests
import os

# Read the prompt from output.txt
with open("output.txt", "r") as file:
    content = file.read()

# Extract the prompt text between <prompt> and </prompt> tags
start_tag = "<prompt>"
end_tag = "</prompt>"
start_index = content.find(start_tag) + len(start_tag)
end_index = content.find(end_tag)
prompt = content[start_index:end_index].strip()


output = replicate.run(
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

# Download the image from the output URL
img_url = output  # Replicate returns a list with the image UR
response = requests.get(img_url)

# Save the image locally
if response.status_code == 200:
    with open("generated_image.jpg", "wb") as f:
        f.write(response.content)
    print(f"Image downloaded successfully and saved as 'generated_image.jpg'")
else:
    print(f"Failed to download image. Status code: {response.status_code}")
