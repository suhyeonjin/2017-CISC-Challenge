#-*- coding:utf-8 -*-
import requests, os, hashlib

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin

from can.can import *


app = Flask(__name__)
CORS(app)

session_list = {};
rand_id = lambda : hashlib.md5(os.urandom(24)).hexdigest()
gen = lambda status, msg: {"status":status, "msg":msg}

'''
    input
        None
    output
        status : request result
        msg : this value that distnguish the user
'''
@app.route('/api/register', methods=["POST"])
def register():
    session_id = rand_id()
    session_list[session_id] = Can()
    result = gen("ok", "%s" % session_id)
    return jsonify(result)


'''
    input
        data : "CAN" log data, seperator is '\n', probably 2000 lines a block
    output
        status : request result
        msg : "CAN" log data current block index value
'''
@app.route('/<session_id>/input', methods=["POST"])
def input(session_id):
    if session_id not in session_list:
        result = gen("no", "<%s> Not Found" % session_id)
    else:
        can_data = request.form["data"]
        if not can_data:
            result = gen("no", "Input Data Error")
        else:
            cur_can = session_list[session_id]
            cur_can.set_data(can_data)
            result = gen("ok", "%d" % cur_can.get_idx())
    return jsonify(result)


'''
    input
        idx : the index value of the "CAN" block to response
    output
        status : request result
        msg : can_block[idx] js data #sugo
'''
@app.route('/<session_id>/output', methods=["POST"])
def output(session_id):
    if session_id not in session_list:
        result = gen("no", "<%s> Not Found" % session_id)
    else:
        can_idx = int(request.form["idx"])
        cur_can = session_list[session_id]
        js_data = cur_can.get_data(can_idx)
        if not js_data:
            result = gen("no", "<%s> No Data" % session_id)
        else:
            result = gen("ok", js_data)
    return jsonify(result)

'''
    input
        None
    output
        status : request result
        msg : "CAN" block of last index
'''
@app.route('/<session_id>/render', methods=["POST", "GET"])
def render(session_id):
    if session_id not in session_list:
        result = gen("no", "<%s> Not Found" % session_id)
    else:
        cur_can = session_list[session_id]
        js_data = cur_can.get_data(cur_can.get_idx())
        if not js_data:
            result = gen("no", "<%s> No Data" % session_id)
        else:
            result = gen("ok", js_data)
    return jsonify(result)

'''
    input
        None
    output
        status : request result
        msg : current "CAN" block index
'''
@app.route('/<session_id>/status', methods=["POST", "GET"])
def status(session_id):
    if session_id not in session_list:
        result = gen("no", "<%s> Not Found" % session_id)
    else:
        cur_can = session_list[session_id]
        result = gen("ok", "%d" % cur_can.get_idx())
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True, debug=True)
