import logging
import matplotlib.pyplot as plt
from keras_cv.models import StableDiffusion
import os

class ImageTextModel:
    def __init__(self, img_width=512, img_height=512, jit_compile=False):
        self.model = StableDiffusion(img_width=img_width, img_height=img_height, jit_compile=jit_compile)
        self.logger = logging.getLogger(__name__)

    def generate_images_from_text(self, text, batch_size=3):
        try:
            images = self.model.text_to_image(text, batch_size=batch_size)
            self.logger.info("Images generated successfully.")
        except Exception as e:
            self.logger.error(f"Error generating images: {e}")
            return None
        return images

    def plot_images(self, images):
        try:
            plt.figure(figsize=(20, 20))
            for i in range(len(images)):
                ax = plt.subplot(1, len(images), i + 1)
                plt.imshow(images[i])
                plt.axis("off")
            plt.show()
            self.logger.info("Images plotted successfully.")
        except Exception as e:
            self.logger.error(f"Error plotting images: {e}")

    def save_images(self, images, folder_path):
        try:
            os.makedirs(folder_path, exist_ok=True)
            for i, image in enumerate(images):
                plt.imsave(os.path.join(folder_path, f"image_{i}.png"), image)
            self.logger.info("Images saved successfully.")
        except Exception as e:
            self.logger.error(f"Error saving images: {e}")
