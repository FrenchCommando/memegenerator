import random
import os
import requests
from flask import Flask, render_template, abort, request
from MemeEngine.MemeEngineFile import MemeEngine
from QuoteEngine.IngestorFile import Ingestor

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']
    quotes_internal = []
    for f in quote_files:
        quotes_internal.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"
    imgs_internal = []
    for root, dirs, files in os.walk(images_path):
        imgs_internal = [os.path.join(root, name) for name in files]

    return quotes_internal, imgs_internal


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """
    image_url = request.form.get('image_url', None)
    body = request.form.get('body', None)
    author = request.form.get('author', None)
    if not body:
        body = "Inspirational Quote"
    if not author:
        author = "Unknown Author"
    path = None
    if image_url:
        img_path = f"./static/{os.path.basename(image_url)}"
        response = requests.get(image_url)
        with open(img_path, 'wb') as f:
            f.write(response.content)
        path = meme.make_meme(img_path=img_path, text=body, author=author)
        os.remove(img_path)
    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
