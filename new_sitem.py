import httpx
from selectolax.parser import HTMLParser

url = 'https://truyenqqvn.com/truyen-moi-cap-nhat/trang-1.html?country=4'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}



def get_chapter(link):
    list = []
    r = httpx.get(link)
    html = HTMLParser(r.text)
    for chapter in html.css('.list_chapter .works-chapter-item'):
        item = {
            chapter.css_first('a').text(strip = True): chapter.css_first('a').attrs['href']
        }

        list.append(item)

    return list

r = httpx.get(url, headers = headers)

html = HTMLParser(r.text)
for manga in html.css('.book_avatar a'):
    chapter = get_chapter(manga.attrs['href'])
    # print(manga.attrs['href'])
    print(chapter)