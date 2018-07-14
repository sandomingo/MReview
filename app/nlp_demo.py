# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)
""" APPID AK SK """
APP_ID = '11535456'
API_KEY = 'Z48smZeQ6Vyxgxv1f9e47UfN'
SECRET_KEY = '1liGIVXWuQlqMYGXZrucVNX47G8HrQdA'

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(API_KEY, SECRET_KEY)
headers = {'Content-Type': 'application/json; charset=UTF-8'}
response = requests.get(host, headers=headers)
response_str = response.text
access_token = json.loads(response_str)['access_token']
query_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag_custom?access_token=%s' % access_token

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/comment_tag', methods=['GET', 'POST'])
def comment_tag():
    comment = request.form['comment']
    type = request.form['type']
    options = {}
    options["type"] = type

    """ 构建查询 """
    data = ('{"text": "%s", "type": %s}'%(comment, type)).encode('gbk')

    """ 带参数调用评论观点抽取 """
    resp = requests.post(query_url, headers={'Content-Type': 'application/json'}, data=data).text
    pretty_resp = json.dumps(json.loads(resp), indent=4, ensure_ascii=False)
    return render_template('comment_tag.html', comment_tag=pretty_resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
