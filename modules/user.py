from flask import Flask, request, render_template
from core.lib import *
from analysis.analysis import check as analysis
import cmds.ptt as ptt
import os
import cmds.ptt_user
from app import *

@app.route('/user')
def users():
    return render_template('user.html')

@app.route('/userq')
def userq():

    url = request.args.get('url')
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
            prate = f'{str(str(round((now.count(2) / len(now)) * 100,2)))}%'
            neurate = f'{str(str(round((now.count(1) / len(now)) * 100,2)))}%'
            negrate = f'{str(str(round((now.count(0) / len(now)) * 100,2)))}%'
            ct = len(now)
            writedata(f'{prate}\t{neurate}\t{negrate}\t{ct}',stable_hash(url + i),'user')

    return ['', s2, prate, neurate, negrate, len(f), preu]


@app.route('/progressu')
def progressu():
    return [f'{psu}',preu]
