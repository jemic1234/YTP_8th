from flask import Flask, request, render_template
from core.lib import *
from analysis.analysis import check as analysis
import cmds.ptt as ptt
import os

from app import app,ps,pre
@app.route('/progress')
def progress():
    return [f'{ps}',pre]

@app.route('/get_len')
def get_len():
    try:
        return str(len(ptt.get(request.args.get('url'))[1]))
    except:
        return ' '
