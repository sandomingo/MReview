# -*- coding: UTF-8 -*-

from aip import AipNlp
import json
import time

""" APPID AK SK """
APP_ID = '11506585'
API_KEY = 'HnN0yHhGevtKHSK5wLu9qndH'
SECRET_KEY = 'qsXCP39wozNaQzXD6pVTrlDyjlah6SCI'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

with open("../data/bose-comments-tag", 'wb') as out:
    with open("../data/bose-comments", "rb") as fobj:
        lines = fobj.readlines()
        for line in lines:
            comment = line.decode()
            print(comment)
            out.write(comment.encode('utf-8'))
            options = {}
            options["type"] = 13
            """ 带参数调用评论观点抽取 """
            try:
                resp = client.commentTag(comment, options)
                sent = client.sentimentClassify(comment)
            except Exception as e:
                resp = e.__str__()
            pretty_resp = json.dumps(resp, indent=4, ensure_ascii=False)
            pretty_sent = json.dumps(sent, indent=4, ensure_ascii=False)
            print(pretty_resp)
            out.write(pretty_resp.encode('utf-8'))
            print(pretty_sent)
            out.write(pretty_sent.encode('utf-8'))
            print(' -------- ')
            out.write(' -------- '.encode('utf-8'))
            time.sleep(0.2)