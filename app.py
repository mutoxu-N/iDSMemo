from enum import Enum, IntEnum
from flask import Flask, Response, jsonify, render_template, request
import memo_data

app = Flask(__name__)
data = memo_data.MemoData()

class Type(IntEnum) :
    NEW = 1
    EDIT = 2
    REMOVE = 3
    CHECK = 4

# root アドレスのアクセス処理
@app.route("/")
def hello():
    return render_template("index.html", memos=data.memo)


# メモがクリックされるとここが実行される
@app.route("/receive", methods=["POST"])
def memo_clicked():
    if request.headers['Content-Type'] != 'application/json':
            print(request.headers['Content-Type'])
            return "ERROR"
            
    js = request.json
    httpRes = 200 # OK used as check
    
    if js["type"] == Type.NEW:
        data.add(js["text"])
        httpRes = 201 # Created

    elif js["type"] == Type.EDIT:
        data.set(js["id"], js["text"])
        httpRes = 202 # Accepted used as edit

    elif js["type"] == Type.REMOVE:
        data.remove(js["id"])
        httpRes = 203 # Non-Authoritative Information used as remove

    # print(js)
    return jsonify(data.memo), httpRes


if __name__ == "__main__":
    # flask 実行
    app.run(host="127.0.0.1", port=8080, debug=True)
