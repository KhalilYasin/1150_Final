import requests
import sys
from PIL import Image, ImageFont, ImageDraw
from docx import Document
from docx.shared import Inches
from pyunsplash import PyUnsplash

# api for unspash
API_KEY = "6fe959d9f7971906d0cb9fa31671d876772c1b841405f91b914f2b55bd838257"
# taco api url
URL = "https://taco-1150.herokuapp.com/random/?full_taco=true"
FONT_FILE = "DejaVuSans.ttf"

# this function is to search for image
def search_image(tag):
    '''
    search and download one image with this tag
    '''
    # authenticate unsplash api

    try:
        py_un = PyUnsplash(api_key=API_KEY)
        search = py_un.search(type_='photos', query=tag)
        photos = [i.link_download for i in search.entries]
        image_request = requests.get(photos[0], verify=False)
        with open("taco.jpg", 'wb') as img:
            img.write(image_request.content)
        return photos[0]
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
        data = requests.get(URL, verify=False)
        data = data.json()
    except:
        print("Error requesting taco API")
        sys.exit(1)
    return data

# used a function to customize document
def create_document(data, image_name, photo_info):
    document = Document()
    # naming and adding heading
    document.add_heading("Random Taco Cookbook", 0)
    # adding a picture
    document.add_picture(image_name, width=Inches(5.5))
    document.add_heading('Credits')
    document.add_paragraph('Taco image: ' + photo_info, style='List Bullet')
    document.add_paragraph('Tacos from: ' + URL, style='List Bullet')
    document.add_paragraph('Code by: Khalil', style='List Bullet')
    for recipe in data:
        document.add_page_break()
        names = ', '.join(recipe[name]['name'] for name in recipe)
        document.add_heading(names, 0)
        for rec in recipe:
            document.add_heading(recipe[rec]['name'], level=1)
            document.add_paragraph(recipe[rec]['recipe'])

    document.save("recipes.docx")


def main():
    p = search_image('taco')
    resize_image()
    recipes = []
    for i in range(5):
        recipes.append(make_request())
    create_document(recipes, 'taco_small.jpg', p)


if __name__ == '__main__':
    main()






