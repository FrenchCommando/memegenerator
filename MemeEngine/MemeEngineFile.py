import os
from PIL import Image, ImageFont, ImageDraw


class MemeEngine:
    def __init__(self, folder_path):
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        self.folder_path = folder_path

    def make_meme(self, img_path, text, author, width=500) -> str:
        im = Image.open(img_path)
        print(im.format, im.size, im.mode)
        h, w = im.size
        if w > width:
            out_h = int(h * width / w)
            im = im.resize((out_h, width))
        font = ImageFont.truetype("arial", 20)
        d1 = ImageDraw.Draw(im)
        d1.text((50, 50), text, fill=(25, 200, 255), font=font)
        d2 = ImageDraw.Draw(im)
        d2.text((100, 100), f"--{author}", fill=(2, 255, 255), font=font)
        out_path = os.path.join(self.folder_path, os.path.basename(img_path))
        im.save(out_path)
        return out_path
