import textwrap

from PIL import Image, ImageDraw, ImageFont

from utils.utilities import Util

TitleColor = (255, 255, 255)
DescriptionColor = (51, 236, 254)


class NewsImage:
    def __init__(self):
        self.primary_font = 'BurbankBigRegular-BlackItalic.otf'
        self.secondary_font = 'BurbankSmall-BlackItalic.otf'

    def generate_image(self, data):
        icon = data

        background = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(background)

        # Image
        news_image = Util.download_image(icon['image'])
        if not news_image:
            return background

        if news_image.width != 1280 or news_image.height != 720:
            news_image = news_image.resize((1280, 720), Image.LANCZOS)
        background.paste(news_image, (0, 0))

        # Title
        title_font_size = 50
        title_font = ImageFont.truetype(f'assets/News/fonts/{self.primary_font}', title_font_size)
        draw.text((25, 520), icon.get('title', '').upper(), TitleColor, font=title_font)

        # Description
        description = icon.get('body')
        news_desc = ""
        if description:
            for desc in description.split("\n"):
                for des in textwrap.wrap(desc, width=56):
                    news_desc += f'\n{des}'
            description = news_desc  # Split the Description
            description_font = ImageFont.truetype(f'assets/News/fonts/{self.secondary_font}', 18)
            draw.multiline_text((25, 560), description,
                                DescriptionColor, font=description_font, spacing=6)
        
        background.save(f"images/{icon['title']}.jpg")