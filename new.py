import httpx
from selectolax.parser import HTMLParser 
import requests

def get_chapter_content(url):
    r = httpx.get(url)
    html = HTMLParser(r.text)
    images = []

    for img in html.css('.content img'):
        images.append(img.attrs['src'])

    return images
    
def downimage(url, filename):
    with open(filename, 'wb') as f:
        im = requests.get(url)
        f.write(im.content)

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

base_url = 'https://m.blogtruyenvn.com'
url = 'https://m.blogtruyenvn.com/33426/co-nang-ma-ca-rong-an-bam'

r = httpx.get(url, headers= headers)
html = HTMLParser(r.text)

chapter_container = html.css('.list-chapter .item')
list = []
for chapter in chapter_container:
    items = {
        chapter.css_first('a span').text(): get_chapter_content(base_url + chapter.css_first('a').attrs['href'])
    }

    for image in items[chapter.css_first('a span').text()]:
        name = str(image).split('?')[0]
        downimage(url = image, filename=name.split('/')[-1])


# import json 
# import base64

# data = {}
# with open('some.gif', mode='rb') as file:
#     img = file.read()
# data['img'] = base64.encodebytes(img).decode('utf-8')

# print(json.dumps(data))