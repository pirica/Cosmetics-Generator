import aiohttp

from PIL import Image
from io import BytesIO


class Util:

    @staticmethod
    async def center_x(foregroundWidth: int, backgroundWidth: int, distanceTop: int = 0):

        return int(backgroundWidth / 2) - int(foregroundWidth / 2), distanceTop

    @staticmethod
    async def ratio_resize(image: Image.Image, maxWidth: int, maxHeight: int):

        ratio = max(maxWidth / image.width, maxHeight / image.height)

        return image.resize(
            (int(image.width * ratio), int(image.height * ratio)), Image.ANTIALIAS
        )

    @staticmethod
    async def download(url: str):

        async with aiohttp.ClientSession(auto_decompress=False) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return Image.open(BytesIO(await response.read())).convert("RGBA")