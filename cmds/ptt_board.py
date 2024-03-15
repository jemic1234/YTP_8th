from core.lib import *
import requests
from bs4 import BeautifulSoup as bs4

def get_boards(x:str = 'https://www.ptt.cc/bbs/index.html'):
    p = get_page_html(x)
    t = parse_page_html(p,'a.board')
    pre = [[i['href'],i.select_one('div.board-title').text] for i in t]
    return pre

template = '''
        <div class="col s12 m3">
          <div class="card blue-grey darken-0">
            <div class="card-content white-text">
              <span class="card-title">[title]</span>
              <p>[url]</p>
            </div>
            <div class="card-action">
              <a href="//www.ptt.cc[url]">Check this</a>
              <a href="/browse?board=[url]">Analysis</a>
            </div>
          </div>
        </div>'''

def get_board(x:str = 'https://www.ptt.cc/bbs/index.html'):
    # for i in range(100): print('\n\n\n')
    p = get_page_html(x)
    t = parse_page_html(p,'a')[10:]
    # pre = [[i['href'],i.select_one('div.board-title').text] for i in t]
    return ([[i['href'],i.text] for i in t if i.text.find('搜尋') == -1])
    # return p

def parse_boards(pre):
    ans = '<div class="row">'
    for i in pre:
        assert len(i) == 2
        ans = ans + f"{template.replace('[url]',i[0]).replace('title',i[1][1:][::-1][1:][::-1])}\n"
    ans = ans  + '</div>'
    return ans

def init():
    print(parse_boards(get_board('https://www.ptt.cc/bbs/NBA/index.html')))