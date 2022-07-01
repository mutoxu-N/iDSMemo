from enum import Enum, IntEnum
from flask import Flask, Response, jsonify, render_template, request
import memo_data

app = Flask(__name__)
data = memo_data.MemoData("memo.ids")

class Type(IntEnum) :
    NEW = 1
    EDIT = 2
    REMOVE = 3
    CHECK = 4
    OPEN = 5 # file open
    UNDO = 6
    REDO = 7

# root アドレスのアクセス処理
@app.route("/")
def hello():
    print(data.filename)
    return render_template("index.html", filename=data.filename, memos=data.memo)


# メモがクリックされるとここが実行される
@app.route("/receive", methods=["POST"])
def memo_clicked():
    if request.headers['Content-Type'] != 'application/json':
            print(request.headers['Content-Type'])
            return "ERROR"
            
    js = request.json
    httpRes = 200 # OK used as check
    
    if js["type"] == Type.NEW:
        if js["text"] != "":
            data.add(js["text"])
        httpRes = 201 # Created

    elif js["type"] == Type.EDIT:
        if js["text"] == "":
            data.remove(js["id"])
        else: 
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
