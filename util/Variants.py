import re
import os
import requests
import textwrap

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter, ImageChops
from colorama import Fore

from util.utilities import ImageUtil


class BaseVar:
    def __init__(self):
        self.primary_font = 'BurbankBigRegular-BlackItalic.otf'
        self.secondary_font = 'BurbankSmall-BlackItalic.otf'

    def draw_background(_, ret: Image, rarity):
        try:
            background = Image.open(f'assets/images/default/card_background_{rarity}.png')
        except FileNotFoundError:
            background = Image.open(f'assets/images/default/card_background_common.png')
        background = background.resize((512, 512), Image.ANTIALIAS)
        ret.paste(background)

    def draw_foreground(_, ret: Image, rarity):
        try:
            foreground = Image.open(f'assets/images/default/card_faceplate_{rarity}.png')
        except FileNotFoundError:
            foreground = Image.open(f'assets/images/default/card_faceplate_common.png')
        ret.paste(foreground, foreground)

    def draw_text_background(_, background: Image, text: str, x: int, y: int, font: ImageFont, fill: tuple):
        blurred = Image.new('RGBA', background.size)
        draw = ImageDraw.Draw(blurred)
        draw.text(xy=(x, y), text=text, fill=fill, font=font)
        blurred = blurred.filter(ImageFilter.BoxBlur(10))

        # Paste soft text onto background
        background.paste(blurred, blurred)

    def draw_preview_image(_, ret: Image, icon):
        """"""
        assetpath = icon['LargePreviewImage']['assetPath']
        url = f'https://benbot.app/api/v1/exportAsset?path={assetpath}'
        r = requests.get(url)
        open('cache/temp.png', 'wb+').write(r.content)
        if url:
            image = Image.open('cache/temp.png')

        image = ImageUtil.ratio_resize(image, 512, 512)
        ret.paste(image, image)

    def draw_display_name(self, ret, c, icon):
        text_size = 32
        text = icon['DisplayName']['finalText'].upper()
        if not text:
            return 0

        font = ImageFont.truetype(f'assets/fonts/{self.primary_font}', size=text_size)
        text_width, text_height = font.getsize(text)
        x = (512 - text_width) / 2
        while text_width > 512 - 4:
            text_size = text_size - 1
            font = ImageFont.truetype(f'assets/fonts/{self.primary_font}', size=text_size)
            text_width, text_height = font.getsize(text)
            x = (512 - text_width) / 2
        y = 425

        self.draw_text_background(ret, text, x, y, font, (0, 0, 0, 215))
        c.text(
            (x, y),
            text,
            (255, 255, 255),
            font=font,
            align='center',
            stroke_width=1,
            stroke_fill=(0, 0, 0)
        )

    def draw_description(self, ret, c, icon):
        text_size = 14
        text = icon['Description']['finalText']
        if not text:
            return 0
        text = text.upper()

        font = ImageFont.truetype(f'assets/fonts/{self.secondary_font}', size=text_size)

        if len(text) > 100:
            
            new_text = ""
            for des in textwrap.wrap(text, width=60):
                new_text += f'{des}\n'
            text = new_text  # Split the Description
            text_width, text_height = font.getsize(text)
            
            
            while text_width / 2 > 512 - 4:
                text_size = text_size - 1
                font = ImageFont.truetype(f'assets/fonts/{self.secondary_font}', size=text_size)
                text_width, text_height = font.getsize(text)

            if len(text.split('\n')) > 2:
                text_width = text_width / 2

            x = (512 - text_width) / 2
            y = 465 - text_height

            c.multiline_text(
                (x, y), 
                text,
                fill='white',
                align='center', 
                font=font, 
            )  
        else:
            text_width, text_height = font.getsize(text)
            x = (512 - text_width) / 2
            while text_width > 512 - 4:
                text_size = text_size - 1
                font = ImageFont.truetype(f'assets/fonts/{self.secondary_font}', size=text_size)
                text_width, text_height = font.getsize(text)
                x = (512 - text_width) / 2
            y = 460

            self.draw_text_background(ret, text, x, y, font, (0, 0, 0, 215))
            c.text(
                (x, y),
                text=text,
                fill='white',
                font=font,
            )

    def draw_to_bottom(self, ret, c, icon):
        if not icon['DisplayName']['finalText'] or not icon['Description']['finalText']:
            return 0

        text_size = 17
        font = ImageFont.truetype('assets/fonts/BurbankBigRegular-Black.otf', size=text_size)
        text = 'ITEM VARIANT'.upper()
        text_width, text_height = font.getsize(text)
        self.draw_text_background(
            ret, text, 8, 512 - 2 * 4 - text_height, font, (0, 0, 0, 215))

        c.text(
            (8, 512 - 2 * 4 - text_height),
            text,
            fill=(167, 184, 188),
            font=font,
            align='left'
        )

    def draw_user_flacing(self, ret):
        cb = Image.open('assets/images/default/PlusSign.png')
        ret.paste(cb, cb)

    def main(self, data):
        icon = data
        try:
            rarity = icon['Rarity']
            rarity = rarity.replace('EFortRarity::', '')
            rarity = rarity = rarity.lower()
        except:
            rarity = 'common'

        height = 512
        ret = Image.new('RGB', (height, height))
        c = ImageDraw.Draw(ret)
        self.draw_background(ret, rarity)
        self.draw_preview_image(ret, icon)
        self.draw_foreground(ret, rarity)
        self.draw_display_name(ret, c, icon)
        self.draw_description(ret, c, icon)
        self.draw_to_bottom(ret, c, icon)
        self.draw_user_flacing(ret)

        ret.save(f'cache/{icon["cosmetic_item"]}.png')
        return ret
