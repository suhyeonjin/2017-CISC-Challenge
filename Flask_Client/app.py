#-*- coding:utf-8 -*-
import os, requests, json, time
from threading import Thread
from itertools import islice
from random import random

from flask import Flask, render_template
from flask import session, jsonify, request, make_response
from flask import redirect, url_for

from detect.refactor import *


API_SERVER = "http://localhost:5000"
API_REG = "api/register"
API_INP = "input"
BLK_CNT = 2000

app = Flask(__name__)
detect = detectCan()
idxCount = [0,0]
perCount = []

normalCnt = 0
fuzzyCnt = 0
dosCnt = 0

def req(url, data=None):
    r = requests.post(url, data=data)
    return json.loads(r.text)

def check_session():
    return session.get("id", None)

def send_data(session_id, path):
    global normalCnt, fuzzyCnt, dosCnt

    url = "%s/%s/%s" % (API_SERVER, session_id,API_INP)
    with open(path) as f:
        prv = None
        d = ""
        cnt = 0
        line_cnt = f.read().count('\n')
        f.seek(0,0)

        while True:
            temp = detect.start_Detact(f.readline().strip())

            #for circle chart
            if "Dos" in temp: dosCnt += 1
            elif "Fuzzy" in temp: fuzzyCnt += 1
            else: normalCnt += 1

            cnt += 1
            if 'Timestamp' in temp:
                cur = int(float(temp.split(' ')[1]))
                tmp = float(temp.split(' ')[1])
            elif temp:
                cur = int(float(temp.split('    ')[0]))
                tmp = float(temp.split(' ')[1])
            else:
                continue

            if prv != None:
                if cnt == line_cnt:
                    d += temp + '\n'
                    r = req(url, data={'data':d})
                    idxCount.append(d.count('\n'))
                    perCount.append(tmp)
                    break

                elif (cur - prv == 1):
                    r = req(url, data={'data':d})
                    idxCount.append(d.count('\n'))
                    perCount.append(tmp)
                    d = ""

            prv = cur
            d += temp + '\n'


@app.route("/", methods=["GET", "POST"])
def index():
    url = "%s/%s" % (API_SERVER, API_REG)
    if request.method == "POST":
        result = req(url)
        s_id = result["msg"]
        path = request.form["path"]
        if result["status"] == "ok" and os.path.isfile(path):
            session["id"] = s_id
            session["path"] = path
            session["check"] = True
        return redirect(url_for('view'))
    return render_template("index.html")



@app.route("/view")
def view():
    if not check_session():
        return redirect(url_for('index'))
    s_id = session.get("id")
    path = session.get("path")
    if session.get("check"):
        th = Thread(target=send_data, args=(s_id, path))
        th.start()
        session["check"] = False

    template_data = {
        'session_id' : s_id,
        'file_path' : path,
        'config' : {"server":API_SERVER }
    }
    return render_template("view.html", **template_data)


#first graph draw
@app.route('/live-data')
def live_data():
    global perCount, idxCount
    if len(perCount) < 1:
        time.sleep(3)
        try:
            data = [perCount.pop(0)*1000, idxCount.pop(0)]
        except:
            time.sleep(3)
            data = [perCount.pop(0)*1000, idxCount.pop(0)]
    else:
        data = [perCount.pop(0)*1000, idxCount.pop(0)]

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/live-count')
def live_count():
    global normalCnt, dosCnt, fuzzyCnt
    data = [normalCnt,dosCnt,fuzzyCnt]
    if len(data) < 2:
        time.sleep(3)

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response



if __name__ == "__main__":
    app.config["SECRET_KEY"] = os.urandom(24)
    app.run(host="0.0.0.0", port=5096, threaded=True, debug=True)
