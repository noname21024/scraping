import httpx
from selectolax.parser import HTMLParser
import time
import json
import csv
from dataclasses import asdict

base_url = 'https://blogtruyenvn.com/'

def get_html(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    r = httpx.get(f'https://blogtruyenvn.com/thumb-{page}', headers = headers)
    try:
        r.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        return False
    html = HTMLParser(r.text)
    return html

def handle_link(html):
    try: 
        return base_url + html.attrs['href']
    except:
        return None
    
def get_infomation(url, sel):
    try:
        r = httpx.get(url)
        html= HTMLParser(r.text)
        info = html.css_first(sel)

        return info.text(strip = True)
    except:
        return None

def get_images(url):
        try:
            images = []
            r = httpx.get(url)
            html = HTMLParser(r.text)
            for image in html.css('#content img'):
                images.append(image.attrs['src'])

            return images
        except:
            return None

def get_tags(url):
    try:
        r = httpx.get(url)
        html = HTMLParser(r.text)
        list = []
        for tag in html.css('span.category a'):
            list.append(tag.text(strip = True))

        return list
    except:
        return None

def get_chapter(url):
    try:
        chapter_list = []
        r = httpx.get(url)
        html = HTMLParser(r.text)

        for chapter in html.css('.list-wrap span a'):
            items = {
                chapter.text(strip = True): get_images(base_url + chapter.attrs['href']) #get_images(chapter.attrs['href'])
            }
            chapter_list.append(items)
        
        return chapter_list
    except:
        return None

def parser(html):
    mangas = html.css('.storyitem')

    for manga in mangas:
        items = {
            'name': manga.css_first('h3.title a').attrs['title'],
            'image': manga.css_first('img').attrs['src'],
            'tags': get_tags(handle_link(manga.css_first('a'))),
            'description': get_infomation(handle_link(manga.css_first('a')), '.content'),
            'chapter': get_chapter(handle_link(manga.css_first('a'))),
        }

        yield items
def export_to_csv(mangas):
    with open('mangas.csv', 'w', newline='', ) as f:
        writer = csv.DictWriter(f, fieldnames=mangas.keys())
        writer.writeheader()
        writer.writerow(mangas)

def export_to_json(mangas, page):
    with open(f'get_mangas_page{page}.json', 'a', encoding='utf-8') as f:
        json.dump(mangas, f, ensure_ascii=False, indent=4)
        f.close()

def main():
    mangas = []

    for x in range(3, 7):
        print(f'Đang lấy dữ liệu từ trang: {x}')
        html = get_html(x)
        if html is False:
            break
        data = parser(html)
        for item in data:
            print(item)
            mangas.append(item)
        export_to_json(mangas, x)


if __name__ == '__main__':
    main()