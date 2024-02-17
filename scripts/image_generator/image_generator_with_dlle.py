from openai import OpenAI
from dotenv import load_dotenv
import base64
import logging
from typing import Literal, Optional, Tuple
import os
import requests
from PIL import Image
from typing import Tuple
from io import BytesIO

class ImageGenerate:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        # Get the OpenAI API key from the environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        # Check if the API key is available
        if not self.api_key:
            raise ValueError("API key is not set. Make sure it is available in your .env file.")
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    @staticmethod
    def generate_images(prompt: str) -> str:
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                quality="hd",
                n=1,
            )
            image_url = response.data[0].url
            logging.info("Image generated successfully.")
            return image_url
        except Exception as e:
            logging.error(f"Error while generating image: {e}")
            return ""

    @staticmethod
    def decode_image(base64_data: str) -> Optional[Image.Image]:
        """
        Converts a base64 image into pillow image object.

        :param base64_data: Textual base64 image data.
        :return: Converted pillow image.
        """
        image_data = base64.b64decode(base64_data)
        image_stream = BytesIO(image_data)
        return Image.open(image_stream)

    @staticmethod
    def download_image(url: str, save_path: str, image_name: str) -> Tuple[str, str]:
        """
        Downloads an image from the provided URL and saves it to the specified location with the given image name.

        :param url: HTTP URL of the image.
        :param save_path: Folder location to save the image.
        :param image_name: Name to save the image with.
        :return: Tuple containing the URL of the image and the path where it is saved.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for non-200 status codes

            # Append .png extension to the image name
            image_name += ".png"

            # Ensure the save path exists, create if not
            os.makedirs(save_path, exist_ok=True)

            # Construct the file path with the image name and extension
            save_file_path = os.path.join(save_path, image_name)

            # Save the image
            with open(save_file_path, 'wb') as f:
                f.write(response.content)

            logging.info(f"Image saved to {save_file_path}")
            return save_file_path

        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download image from {url}: {e}") from e

        except OSError as e:
            raise RuntimeError(f"Error occurred while saving the image: {e}") from e
