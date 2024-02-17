import os
import requests
from PIL import Image
from io import BytesIO
import base64
import logging
from typing import Literal, Optional, Tuple
from urllib.parse import urlparse
from pydantic import HttpUrl

import replicate  # Assuming this is a custom module in your project

# Configurations
os.environ["REPLICATE_API_TOKEN"] = "r8_H9QNHzRFhByXizFAkbwHYUgLaAREq5C2uor8H"
logging.basicConfig(level=logging.INFO)

class ImageGenerater:
    def __init__(self, asset_suggestions: dict) -> None:
        self.asset_suggestions = asset_suggestions

    def generate_images(self, store_location: str = './images') -> dict:
        generated_images = {}
        for frame, elements in self.asset_suggestions.items():
            if frame.startswith('frame'):
                generated_images[frame] = []
                for type, description in elements.items():
                    downloaded_image = ImageGenerater.download_image(HttpUrl(description), store_location, f"{frame}_{type.replace(' ', '_')}.png")
                    generated_images[frame].append((type, *downloaded_image))

        return generated_images

    @staticmethod
    def generate_image(prompt: str, performance_selection: Literal['Speed', 'Quality', 'Extreme Speed'] = "Extreme Speed",
                       aspect_ratios_selection: str = "1024*1024", image_seed: int = 1234, sharpness: int = 2) -> Optional[dict]:
        """
        Generates an image based on the given prompt and settings.

        :param prompt: Textual description of the image to generate.
        :param performance_selection: Choice of performance level affecting generation speed and quality.
        :param aspect_ratio: The desired aspect ratio of the generated image.
        :param image_seed: Seed for the image generation process for reproducibility.
        :param sharpness: The sharpness level of the generated image.
        :return: The generated image or None if an error occurred.
        """
        try:
            output = replicate.run(
                "konieshadow/fooocus-api-anime:a750658f54c4f8bec1c8b0e352ce2666c22f2f919d391688ff4fc16e48b3a28f",
                input={
                    "prompt": prompt,
                    "performance_selection": performance_selection,
                    "aspect_ratios_selection": aspect_ratios_selection,
                    "image_seed": image_seed,
                    "sharpness": sharpness
                }
            )
            logging.info("Image generated successfully.")
            return output
        except Exception as e:
            logging.error(f"Failed to generate image: {e}")
            return None

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

            # Get the file extension from the URL
            image_extension = os.path.splitext(url)[-1]

            # Ensure the save path exists, create if not
            os.makedirs(save_path, exist_ok=True)

            # Check if the image name already exists in the save path
            existing_files = [f for f in os.listdir(save_path) if f.startswith(image_name)]
            if existing_files:
                # Append a suffix to the image name to make it unique
                image_name = f"{image_name}_{len(existing_files) + 1}"

            # Construct the file path with the image name and extension
            save_file_path = os.path.join(save_path, f"{image_name}{image_extension}")

            # Save the image
            with open(save_file_path, 'wb') as f:
                f.write(response.content)

            logging.info(f"Image saved to {save_file_path}")
            return save_file_path

        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download image from {url}: {e}") from e

        except OSError as e:
            raise RuntimeError(f"Error occurred while saving the image: {e}") from e


# if __name__ == "__main__":
#     a = {
#     "frame_1": {
#         "Animated Element": "A high-resolution 3D Coca-Cola bottle center-screen, bubbles rising to the top, transitioning into a sleek DJ turntable with a vinyl record that has the Coke Studio logo.",
#     },
#     "frame_2": {
#         "CTA Text": "'Mix Your Beat' in bold, playful font pulsating to the rhythm of a subtle background beat, positioned at the bottom of the screen."
#     },
#     "explanation": "This variation emphasizes the joy and interactivity of music mixing, with each frame building on the last to create a crescendo of engagement. The 3D bottle-to-turntable animation captures attention, the interactive beat mixer sustains engagement, and the vibrant animations encourage sharing, aligning with the campaign's objectives of engagement and message recall."
#     }
#     test = ImageGenerater(a)
#     # test.generate_images()
#     test.download_image(url='https://replicate.delivery/pbxt/wql2Dj7yR16bF5RYzKPnwWsLigfzeVneAAkk8BfjXRHbTAeSC/8255c049-117e-49e4-a47b-983fe266c202.png',
#     save_path='../storedboard_assets/frame1/',
#     image_name='background_with_small_aspect_ratio')
