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

<code>

if __name__ == '__main__':
    app.run(port=8000, debug=True)
