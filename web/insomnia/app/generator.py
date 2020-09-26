"""Generate meme based on passed config """
import io
import yaml
from PIL import Image, ImageDraw, ImageFont

MEMES = {
    "doge": "/opt/memes/doge.jpg",
    "TrollFace": "/opt/memes/TrollFace.jpg",
    "Dolan": "/opt/memes/Dolan.jpg",
    "YUNO": "/opt/memes/YUNO.jpg"
}

class MemeNotFoundError(Exception):
    pass

class MemeGenerator:
    def __init__(self, config_yaml):
        config = yaml.full_load(config_yaml)

        self.top = config['top']
        self.bottom = config['bottom']
        self.meme = config['meme']

        if self.meme not in MEMES:
            raise MemeNotFoundError()

        self._load_image()

    def _load_image(self):
        _filepath = MEMES[self.meme]
        
        self.image = Image.open(_filepath).convert('RGBA')
        
    def build(self):
        image_draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("/opt/font/meme.ttf", 64)

        W, H = self.image.size
        w_top, _ = image_draw.textsize(self.top, font=font)
        w_bottom, _ = image_draw.textsize(self.bottom, font=font)

        image_draw.text(((W-w_top)/2, 0.1*H), self.top, font=font, fill='red')
        image_draw.text(((W-w_bottom)/2, 0.8*H), self.bottom, font=font, fill='red')

        self.image_stream = io.BytesIO()
        self.image.save(self.image_stream, format="png")
        self.image_stream.seek(0)
