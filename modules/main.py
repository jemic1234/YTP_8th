from flask import Flask, request, render_template
from core.lib import *
from analysis.analysis import check as analysis
import cmds.ptt as ptt
import os

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/craw')
def craw():
    url = request.args.get('url')
    limit = request.args.get('limit') or '1000000000'
    model = request.args.get('model')
    global ps
    global pre
    try:
        s1, s2, prate, neurate, negrate, f, pre = getdata(stable_hash(url + str(limit) + str(model)),'result').split('\t')
        ps = 100
        return [s1, s2, prate, neurate, negrate, f, pre]
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
    s2 = ''
    s1 = str(a_content) 
    for i in comment:
        f.append(analysis(i, model))
        try:
            pr, ne, ng, ct = getdata(stable_hash(url + username[len(f) - 1]),'user').split('\t')
            username[len(f) - 1] += f'\t | \t {pr} \t {ne} \t {ng} \t {ct}'
        except:
            pass
        pre = pre + f'<a id=\'username\' href=\'user?url={url}&user={username[len(f) - 1]}\' class=\'{["WA","RE","AC"][f[len(f) - 1]]}\'> {username[len(f) - 1]} </a><br>' + f'<a class=\'{["WA","RE","AC"][f[len(f) - 1]]}\'> {i} </a><br>'
        ps = int((len(f) / min(len(comment),limit)) * 10000) / 100

        for j in range(3):
            if f.count(j) >= f.count((j + 1) % 3) and f.count(j) >= f.count((j + 2) % 3):
                s2 = ['NEGATIVE','NEUTRAL','POSITIVE'][j]
        prate = f'{str(str(round((f.count(2) / len(f)) * 100,2)))}%'
        neurate = f'{str(str(round((f.count(1) / len(f)) * 100,2)))}%'
        negrate = f'{str(str(round((f.count(0) / len(f)) * 100,2)))}%'
        writedata(f'{s1}\t{s2}\t{prate}\t{neurate}\t{negrate}\t{len(f)}\t{pre}',stable_hash(url + str(len(f)) + str(model)),'result')
        if len(f) == limit:
            break
    writedata(f'{s1}\t{s2}\t{prate}\t{neurate}\t{negrate}\t{len(f)}\t{pre}',stable_hash(url + str(limit) + str(model)),'result')
    return [s1, s2, prate, neurate, negrate, len(f), pre]
