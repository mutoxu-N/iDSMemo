from tkinter import filedialog
from flask import Flask, Response, jsonify, render_template, request
from memo_data import MemoData
from memo_config import MemoConfig
from type import Type
import os

app = Flask(__name__)
config = MemoConfig()
data = MemoData(config.url)



# root アドレスのアクセス処理
@app.route("/")
def root():
    """
    メイン画面を出力
    """
    return render_template("index.html", filename=data.filename, memos=data.memo)


# メモがクリックされるとここが実行される
@app.route("/receive", methods=["POST"])
def received():
    """
    JavaScriptからデータを受信したときの処理
    """
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
            data.edit(js["id"], js["text"])

    elif js["type"] == Type.REMOVE:
        data.remove(js["id"])

    # TODO 2回目以降、新規ファイル作成やファイルを開くのができなくなる。Electronでファイルを読み込んで通信するのが吉
    elif js["type"] == Type.F_NEW:
        url = filedialog.asksaveasfilename(filetypes = [('メモファイル', '*.ids')], initialdir = config.dir)
        if url != "":
            config.setDir()
            data.load(config.url)

    elif js["type"] == Type.F_OPEN:
        url = filedialog.askopenfilename(filetypes = [('メモファイル', '*.ids')], initialdir = config.dir)
        if url != "":
            if os.path.exists(url):
                config.setDir(url)
            else:
                config.setDir(url)
            data.load(config.url)

    elif js["type"] == Type.UNDO:
        data.undo()

    elif js["type"] == Type.REDO:
        data.redo()
        
    return jsonify([data.filename, data.memo]), 200


if __name__ == "__main__":
    # flask 
    app.run(host="127.0.0.1", port=8080, debug=True)
