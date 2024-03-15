from core.lib import *
import cmds.ptt_board as board
import cmds.ptt as ptt
ptt_url = 'https://www.ptt.cc'

def get(url: str, target: str):
    url = '/'.join(url.split('/')[::-1][1:][::-1]) + '/index.html'
    # print(url)
    ans = []
    for i in board.get_board(url):
        _, comment,username = ptt.get(ptt_url + i[0])
        assert(len(comment) == len(username))
        for j in range(len(username)):
            if target == '*' or target == ' ':
                ans.append([i[0],comment[j],username[j]])
                continue
            if username[j].find(target) != -1:
                ans.append([i[0],comment[j]])
        print(i[0])
    print(ans)
    return ans