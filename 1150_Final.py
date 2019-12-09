import requests
import sys
import urllib.request
from PIL import Image, ImageFont, ImageDraw
from docx import Document
from docx.shared import Inches
from pyunsplash import PyUnsplash

# api for unspash
API_KEY = "6fe959d9f7971906d0cb9fa31671d876772c1b841405f91b914f2b55bd838257"
# taco api url
URL = "https://taco-1150.herokuapp.com/random/?full_taco=true"
FONT_FILE = "DejaVuSans.ttf"


def search_image(tag):
    '''
    search and download one image with this tag
    '''
    # authenticate unsplash api
    try:
        py_un = PyUnsplash(api_key=API_KEY)
        search = py_un.search(type_='photos', query=tag)
        photos = [i.link_download for i in search.entries]
        urllib.request.urlretrieve(photos[0], 'taco.jpg')
    except:
        print("Error in search_image")
        sys.exit(1)


def resize_image():
    '''
    this function resize the image and write Random Taco CookBook
    '''
    try:
        im = Image.open('taco.jpg')
    except IOError:
        print("Error opening image")
        sys.exit(1)
    width, height = im.size
    ratio = height / width
    # set image to max 800 in width and height
    if (width > height):
        width = 800
        height = int(ratio * 800)
    else:
        height = 800
        width = int(800 / ratio)
    im = im.resize((width, height), Image.ANTIALIAS)
    font = ImageFont.truetype(FONT_FILE, 40)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), "Random Taco Cookbook", (255, 255, 255), font=font)
    im.save('taco_small.jpg', format='JPEG')


def make_request():
    '''
    this function returns data from taco api
    '''
    try:
        data = requests.get(URL)
        data = data.json()
    except:
        print("Error requesting taco API")
        sys.exit(1)
    return data


def main():
    search_image('taco')
    resize_image()
    recipes = []
    for i in range(5):
        recipes.append(make_request())


if __name__ == '__main__':
    main()






