from flask import Flask, request, render_template
from core.lib import *
from analysis.analysis import check as analysis
import cmds.ptt as ptt
import cmds.ptt_board as board
import os
from app import *

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




