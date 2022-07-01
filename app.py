from enum import IntEnum
from tkinter import filedialog
from flask import Flask, Response, jsonify, render_template, request
from memo_data import MemoData
from memo_config import MemoConfig
import os

app = Flask(__name__)
config = MemoConfig()
data = MemoData(config.url)

class Type(IntEnum) :
    NEW = 1
    EDIT = 2
    REMOVE = 3
    CHECK = 4
    F_OPEN = 5
    F_NEW = 6 
    UNDO = 7
    REDO = 8
    ALL_REMOVE = 9

# root アドレスのアクセス処理
@app.route("/")
def hello():
    return render_template("index.html", filename=data.filename, memos=data.memo)


# メモがクリックされるとここが実行される
@app.route("/receive", methods=["POST"])
def memo_clicked():
    if request.headers['Content-Type'] != 'application/json':
            print(request.headers['Content-Type'])
            return "ERROR"
            
    js = request.json
    
    if js["type"] == Type.NEW:
        if js["text"] != "":
            data.add(js["text"])

    elif js["type"] == Type.EDIT:
        if js["text"] == "":
            data.remove(js["id"])
        else: 
            data.set(js["id"], js["text"])

    elif js["type"] == Type.REMOVE:
        data.remove(js["id"])

    # TODO 2回目以降、新規ファイル作成やファイルを開くのができなくなる。Electronでファイルを読み込んで通信するのが吉
    elif js["type"] == Type.F_NEW:
        config.setDir(filedialog.asksaveasfilename(filetypes = [('メモファイル', '*.ids')], initialdir = config.dir))
        data.load(config.url)

    elif js["type"] == Type.F_OPEN:
        url = filedialog.askopenfilename(filetypes = [('メモファイル', '*.ids')], initialdir = config.dir)
        if os.path.exists(url):
            config.setDir(url)
        else:
            config.setDir(url)
        data.load(config.url)
        
    # print(js)
    return jsonify([data.filename, data.memo]), 200


if __name__ == "__main__":
    # flask 
    app.run(host="127.0.0.1", port=8080, debug=True)
