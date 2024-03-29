from core.lib import *
import requests
from bs4 import BeautifulSoup as bs

def get(url: str):
    html = get_page_html(url)
    soup = bs(html,'html.parser')
    sp = soup.find(id = 'main-content')
    content = sp.text
    content = content[:content.find('\n\n--\n')]
    sp = sp.select('div.push')
    comment = []
    name = []
    last = ''
    print(f'parsing {url}')
    for i in sp:
        try:
            username, inside = i.select('span')[1].text.replace(': ',''), i.select('span')[2].text.replace(': ','')
            if inside.find('http') != -1:
                continue
            if username == last:
                comment[len(comment) - 1] += inside
            else:
                comment.append(inside)
                name.append(username)
                last = username
        except:
            pass
    return content, comment, name