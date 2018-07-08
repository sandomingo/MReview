# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request
from aip import AipNlp
import json

app = Flask(__name__)
""" APPID AK SK """
APP_ID = '11506585'
API_KEY = 'HnN0yHhGevtKHSK5wLu9qndH'
SECRET_KEY = 'qsXCP39wozNaQzXD6pVTrlDyjlah6SCI'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/comment_tag', methods=['GET', 'POST'])
def comment_tag():
    comment = request.form['comment']
    type = request.form['type']
    options = {}
    options["type"] = type

    """ 带参数调用评论观点抽取 """
    resp = client.commentTag(comment, options)
    pretty_resp = json.dumps(resp, indent=4, ensure_ascii=False)
    print(pretty_resp)
    return render_template('comment_tag.html', comment_tag=pretty_resp)


if __name__ == '__main__':
    app.run()
