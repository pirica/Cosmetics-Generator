from PIL import ImageFont, Image
from colorama import *
from math import ceil, sqrt
from typing import Union
from io import BytesIO
from datetime import datetime

import aiohttp
import os
import glob
import requests



class Util:
    @staticmethod
    def iso_to_human(date: str):
        """Return the provided ISO8601 timestamp in human-readable format."""

        try:
            # Unix-supported zero padding removal
            return datetime.strptime(date, "%Y-%m-%d").strftime("%A, %B %-d, %Y")
        except ValueError:
            try:
                # Windows-supported zero padding removal
                return datetime.strptime(date, "%Y-%m-%d").strftime("%A, %B %#d, %Y")
            except Exception as e:
                raise e

    @staticmethod
    async def center_x(foregroundWidth: int, backgroundWidth: int, distanceTop: int = 0):

        return int(backgroundWidth / 2) - int(foregroundWidth / 2), distanceTop

    @staticmethod
    async def font(
            size: int,
            font: str,
            directory: str = "assets/fonts/",
    ):

        try:
            return ImageFont.truetype(f"{directory}{font}", size)
        except OSError:
            print(
                Fore.RED + f"{font} not found, defaulted font to BurbankBigCondensed-Black.otf")

            return ImageFont.truetype(f"{directory}BurbankBigCondensed-Black.otf", size)
        except Exception as e:
            print(Fore.RED + f"Failed to load font, {e}")

    @staticmethod
    async def fit_text_x(
            text: str,
            size: int,
            maxSize: int,
            font_name: str,
    ):

        font = await Util.font(size, font_name)
        textWidth, _ = font.getsize(text)

        while textWidth >= maxSize:
            size = size - 1
            font = await Util.font(size, font_name)
            textWidth, _ = font.getsize(text)

        return await Util.font(size, font_name), textWidth

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


class ImageUtil:
    async def new_image_generator(self, data, save_as, assets_type=None):

        if len(data) > 0:

            for i in data:
                print(Fore.BLUE + f'Generating {i["name"]}')


            if assets_type is not None:
                x = []
                for i in data:
                    if 'backendType' in i and i["backendType"] == assets_type:
                        x.append(i)
                    elif 'type' in i and i['type']['value'] == assets_type:
                        x.append(i)
            else:
                x = data

            if len(x) == 0:
                return 0

            row_n = len(x)
            if os.path.isfile(f'assets/images/{self.watermarkIcon}'):
                row_n += 1

            rowslen = ceil(sqrt(row_n))
            columnslen = round(sqrt(row_n))

            mode = "RGB" if '.jpg' in save_as else "RGBA"
            px = 512 if '.jpg' in save_as else 516
            add = 4 if px == 516 else 0

            rows = (rowslen * px - 4) if px == 516 else rowslen * px
            columns = (columnslen * px - 4) if px == 516 else columnslen * px

            image = Image.new(mode, (rows, columns))

            i = 0

            for y in x:
                card = Image.open(f'images/{y["id"]}.png')
                if card is not None:
                    image.paste(
                        card,
                        ((0 + ((i % rowslen) * (card.width + add))),
                         (0 + ((i // rowslen) * (card.height + add))))
                    )

                    i += 1

            if os.path.isfile(f'assets/images/{self.watermarkIcon}'):
                card = Image.open(f'assets/images/{self.watermarkIcon}')
                card = await Util.ratio_resize(card, 512, 512)
                image.paste(
                    card,
                    ((0 + ((i % rowslen) * (card.width + add))),
                     (0 + ((i // rowslen) * (card.height + add))))
                )

            try:
                image.save(save_as)
            except Exception as e:
                print(e)

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
            (int(image.width * ratio), int(image.height * ratio)), Image.ANTIALIAS
        )

    @staticmethod
    def merge_icons(datas: Union[list, None] = None, save_as: str = 'merge.jpg'):
        if not datas:
            datas = [Image.open(i) for i in glob.glob('Cache/images/*.png')]

        row_n = len(datas)
        rowslen = ceil(sqrt(row_n))
        columnslen = round(sqrt(row_n))

        mode = "RGB"
        px = 512

        rows = rowslen * px
        columns = columnslen * px
        image = Image.new(mode, (rows, columns))

        i = 0

        for card in datas:
            image.paste(
                card,
                ((0 + ((i % rowslen) * card.width)),
                 (0 + ((i // rowslen) * card.height)))
            )

            i += 1

        if save_as and len(save_as) > 4:
            image.save(f"Cache/{save_as}")

        return image


    @staticmethod
    def merge_icons(datas: Union[list, None] = None, save_as: str = '.png'):
        if not datas:
            datas = [Image.open(i) for i in glob.glob('newc/*.png')]

        print('\nMerging images...')
        row_n = len(datas)
        rowslen = ceil(sqrt(row_n))
        columnslen = round(sqrt(row_n))

        mode = "RGB"
        px = 512

        rows = rowslen * px
        columns = columnslen * px
        image = Image.new(mode, (rows, columns))

        i = 0

        for card in datas:
            image.paste(
                card,
                ((0 + ((i % rowslen) * card.width)),
                 (0 + ((i // rowslen) * card.height)))
            )

            i += 1

        if save_as and len(save_as) > 4:
            image.save(f"images/{save_as}")

        return image