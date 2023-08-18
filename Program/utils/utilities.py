import requests

from PIL import Image

class Util:

    @staticmethod
    def download_image(url):
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            return Image.open(res.raw).convert('RGBA')
    
    @staticmethod
    def center_x(foreground_width: int, background_width: int, height: int):
        """Return the tuple necessary for horizontal centering and an optional vertical distance."""

        return int(background_width / 2) - int(foreground_width / 2), height

    @staticmethod
    def ratio_resize(image: Image.Image, max_width: int, max_height: int):
        """Resize and return the provided image while maintaining aspect ratio."""

        ratio = max(max_width / image.width, max_height / image.height)

        return image.resize(
            (int(image.width * ratio), int(image.height * ratio)), Image.LANCZOS
        )