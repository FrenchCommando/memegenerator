# from PIL import Image, ImageFont, ImageDraw


class MemeEngine:
    def __init__(self, folder_path):
        pass

    def make_meme(self, img_path, text, author, width=500) -> str:
        im = Image.open(img_path)
        print(im.format, im.size, im.mode)
        pass
