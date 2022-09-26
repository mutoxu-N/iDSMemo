from tkinter import filedialog
from flask import Flask, Response, jsonify, render_template, request
from memo_data import MemoData
from memo_config import MemoConfig
from type import Type
import os, requests, json

app = Flask(__name__)
config = MemoConfig()
data = MemoData(config.url)



# root アドレスのアクセス処理
@app.route("/")
def root():
    """
    メイン画面を出力
    """
    if config.url is not None:
        return render_template("index.html", filename=data.filename, memos=data.memo)
    else:
        return render_template("index.html", filename="", memos=[])


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

    elif js["type"] == Type.F_NEW:
        if config.url is None:
            res = requests.get("http://127.0.0.1:8081/electron", headers={'content-type': 'application/json'},
                data=json.dumps({"type": Type.F_NEW, "url": ""}))
        else:
            res = requests.get("http://127.0.0.1:8081/electron", headers={'content-type': 'application/json'},
                data=json.dumps({"type": Type.F_NEW, "url": config.dir}))

        url = res.content.decode()
        if url != "":
            config.setDir(url)
            data.load(url)

    elif js["type"] == Type.F_OPEN:
        if config.url is None:
            res = requests.get("http://127.0.0.1:8081/electron", headers={'content-type': 'application/json'},
                data=json.dumps({"type": Type.F_OPEN, "url": ""}))
        else:
            res = requests.get("http://127.0.0.1:8081/electron", headers={'content-type': 'application/json'},
                data=json.dumps({"type": Type.F_OPEN, "url": config.dir}))
        url = res.content.decode()
        if url != "":
            if os.path.exists(url):
                config.setDir(url)
                data.load(config.url)

    elif js["type"] == Type.UNDO:
        data.undo()

    elif js["type"] == Type.REDO:
        data.redo()

    elif js["type"] == Type.ALL_REMOVE:
        data.removeAll()

    elif js["type"] == Type.GROUP:
        data.group(js["group"])
        
    elif js["type"] == Type.CHECK and config.url is None:
        return jsonify([]), 200
        
    return jsonify([data.filename, data.memo]), 200


if __name__ == "__main__":
    # flask 
    app.run(host="127.0.0.1", port=8080, debug=True)
