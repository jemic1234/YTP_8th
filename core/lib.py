import os
import requests
import json
from bs4 import BeautifulSoup as bs

DATA_PATH = os.getcwd().replace('\\', '/')+"/data/"
MOUDLE_PATH = os.getcwd().replace('\\', '/')+"/dataMoudle/"

def get_page_html(url: str):
    header = {'cookie': 'over18=1'}
    response = requests.get(url, headers=header)
    return response.text

def parse_page_html(html,tag):
    soup = bs(html, 'html.parser')
    problems = soup.select(tag)
    return problems

def write_to_file(x: str,name: str):
    f = open(name,'w',encoding = 'UTF-8')
    f.write(a)
    f.close()
    return

def read_from_file(name: str) -> str:
    with open(name,'r') as f:
        ans = ''
        for i in f:
            ans = ans + i
        f.close()
    return ans

def getdata(dataname,dataType):
    with open(DATA_PATH+str(dataType)+"/"+str(dataname)+".json", "r", encoding="utf-8") as file:
        data = json.load(file)
    file.close()
    return data
    

def writedata(data, path, dataType): 
    file = open(DATA_PATH+str(dataType)+"/"+str(path)+".json", "w")
    json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii = False)
    file.close()

def stable_hash(x: str) -> int:
    now = x + '%&*(&%$)'
    R = (1 << ((1 << 7) - 1)) - 1
    T = 10 ** 9 + 7
    tt = 1
    t = 0
    ans = 0
    for i in now:
        tt = (tt * T) % R
        ans = (ans + ord(i) * tt) % R
    return ans
    