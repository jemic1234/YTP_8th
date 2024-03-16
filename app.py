from flask import Flask, request, render_template
from core.lib import *
from analysis.analysis import check as analysis
import cmds.ptt as ptt
import cmds.ptt_board as board
import cmds.ptt_user
import os

app = Flask(__name__, static_folder='static')
ps = 0
pre = ''
psu = 0
preu = ''

# browse.py


@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/ptt_board')
def ptt_board():
    s = request.args.get('board') or '1'
    if s != '1' and not s.endswith('index.html'):
        return 'analysis'
    if s == '1': return board.parse_boards(board.get_boards());
    else: 
        print('https://www.ptt.cc' + s)
        return board.parse_boards(board.get_board('https://www.ptt.cc' + s));






# main.py


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/craw')
def craw():
    url = request.args.get('url')
    brl = '/'.join(url.split('/')[::-1][1:][::-1]) + '/index.html'
    limit = request.args.get('limit') or '1000000000'
    model = request.args.get('model')
    global ps
    global pre
    try:
        s1, s2, prate, neurate, negrate, f, pre, zz = getdata(stable_hash(url + str(limit) + str(model)),'result').split('\t')
        ps = 100
        return [s1, s2, prate, neurate, negrate, f, pre, zz]
    except:
        pass
    limit = int(limit)
    ps = 0
    content, comment, username = ptt.get(url)

    assert(type(content) is str)
    for i in comment: assert(type(i) is str)

    a_content = ['NEGATIVE','NEUTRAL','POSITIVE'][analysis(content, model)]
    ps = 1

    pre = ''
    f = []
    rz = []
    s2 = ''
    zz = ''
    s1 = str(a_content) 
    for i in comment:
        f.append(analysis(i, model))
        nz = username[len(f) - 1]
        try:
            pr, ne, ng, ct = getdata(stable_hash(brl + username[len(f) - 1]),'user').split('\t')
            username[len(f) - 1] += f'\t | \t {pr} \t {ne} \t {ng} \t {ct}'
            if f[len(f) - 1] == 2: rz.append(float(pr[::-1][1:][::-1]));
        except:
            pass
        pre = pre + f'<a id=\'username\' href=\'user?url={url}&user={nz}\' class=\'{["WA","RE","AC"][f[len(f) - 1]]}\'> {username[len(f) - 1]} </a><br>' + f'<a class=\'{["WA","RE","AC"][f[len(f) - 1]]}\'> {i} </a><br>'
        ps = int((len(f) / min(len(comment),limit)) * 10000) / 100

        for j in range(3):
            if f.count(j) >= f.count((j + 1) % 3) and f.count(j) >= f.count((j + 2) % 3):
                s2 = ['NEGATIVE','NEUTRAL','POSITIVE'][j]
        prate = f'{str(str(round((f.count(2) / len(f)) * 100,2)))}%'
        neurate = f'{str(str(round((f.count(1) / len(f)) * 100,2)))}%'
        negrate = f'{str(str(round((f.count(0) / len(f)) * 100,2)))}%'
        zz = f'{str(str(round((sum(rz) / len(rz)),2)))}%' if len(rz) != 0 else -1
        writedata(f'{s1}\t{s2}\t{prate}\t{neurate}\t{negrate}\t{len(f)}\t{pre}\t{zz}',stable_hash(url + str(len(f)) + str(model)),'result')
        if len(f) == limit:
            break
    
    writedata(f'{s1}\t{s2}\t{prate}\t{neurate}\t{negrate}\t{len(f)}\t{pre}\t{zz}',stable_hash(url + str(limit) + str(model)),'result')
    return [s1, s2, prate, neurate, negrate, len(f), pre, zz]


# requests.py

@app.route('/progress')
def progress():
    return [f'{ps}',pre]

@app.route('/get_len')
def get_len():
    try:
        return str(len(ptt.get(request.args.get('url'))[1]))
    except:
        return ' '


# user.py


@app.route('/user')
def users():
    return render_template('user.html')

@app.route('/userq')
def userq():

    url = request.args.get('url')
    brl = '/'.join(url.split('/')[::-1][1:][::-1]) + '/index.html'
    user = request.args.get('user') or ' '
    model = request.args.get('model')
    print(url,model);
    global psu
    global preu
    psu = 0
    if user == '*':
        namecount = {}
        ans = ''
        comment = cmds.ptt_user.get(url,'*')
        for i in comment:
            namecount[i[2]] = namecount.get(i[2],0) + 1
        for j in namecount:
            ans = ans + j + ' ' + str(namecount.get(j)) + '<br>' + '\n'
        preu = ans
        psu = 100
        return ans
    comment = cmds.ptt_user.get(url,user)

    # for i in comment: assert(type(i) is str)


    
    preu = ''
    f = []
    s2 = ''
    userate = {}
    prate, neurate, negrate = 0, 0, 0
    for i in comment:
        f.append(analysis(i[1], model))
        preu = preu + f'<a href=\'{cmds.ptt_user.ptt_url}{i[0]}\' class=\'{["WA","RE","AC"][f[len(f) - 1]]}\'> {i[1]} </a><br>'
        if user == ' ':
            tmp = userate.get(i[2],[])
            tmp.append(f[len(f) - 1])
            userate[i[2]] = tmp
        psu = int((len(f) / len(comment)) * 10000) / 100

        for j in range(3):
            if f.count(j) >= f.count((j + 1) % 3) and f.count(j) >= f.count((j + 2) % 3):
                s2 = ['NEGATIVE','NEUTRAL','POSITIVE'][j]
        prate = f'{str(str(round((f.count(2) / len(f)) * 100,2)))}%'
        neurate = f'{str(str(round((f.count(1) / len(f)) * 100,2)))}%'
        negrate = f'{str(str(round((f.count(0) / len(f)) * 100,2)))}%'
    
    if user == ' ':
        for i in userate:
            now = userate.get(i,[])
            dprate = f'{str(str(round((now.count(2) / len(now)) * 100,2)))}%'
            dneurate = f'{str(str(round((now.count(1) / len(now)) * 100,2)))}%'
            dnegrate = f'{str(str(round((now.count(0) / len(now)) * 100,2)))}%'
            ct = len(now)
            writedata(f'{dprate}\t{dneurate}\t{dnegrate}\t{ct}',stable_hash(brl + i),'user')

    return ['', s2, prate, neurate, negrate, len(f), preu]


@app.route('/progressu')
def progressu():
    return [f'{psu}',preu]




if __name__ == '__main__':
    app.run(port=8000, debug=True)
