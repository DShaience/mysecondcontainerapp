# TODO: move these utils to research. it is more of a research utils than source.

import json
# from io import BytesIO
# from base64 import encodebytes

import base64
from PIL import Image
import io


def read_json_file(file_path):
    """Read a JSON file and return its content as a Python dictionary."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
    except Exception as e:
        print(f"An error occurred: {e}")



def image_to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def rescale_and_pad_image(image_b64, target_size, fill_color=(128, 128, 128)):
    # Decode the base64 image
    img_data = base64.b64decode(image_b64)
    img = Image.open(io.BytesIO(img_data))
    
    # Calculate the aspect ratio of the original and target image
    img_aspect = img.width / img.height
    target_width, target_height = target_size
    target_aspect = target_width / target_height
    
    # Determine new width and height that fit within target while preserving aspect ratio
    if img_aspect > target_aspect:
        # Image is wider relative to the target, fit by width
        new_width = target_width
        new_height = int(target_width / img_aspect)
    else:
        # Image is taller relative to the target, fit by height
        new_height = target_height
        new_width = int(target_height * img_aspect)
    
    # Resize the image to the new dimensions
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create a new image with the target size and gray background
    new_img = Image.new("RGB", (target_width, target_height), fill_color)
    
    # Paste the resized image onto the center of the new background
    offset = ((target_width - new_width) // 2, (target_height - new_height) // 2)
    new_img.paste(img_resized, offset)
    
    # Convert the final image back to base64
    # return image_to_base64(new_img)
    return new_img  # leave it as PIL.Image



def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


