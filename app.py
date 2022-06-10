from __future__ import print_function
from os import remove
from flask import Flask, Response, jsonify, render_template, request
import memo_data

app = Flask(__name__)
data = memo_data.MemoData()

# root アドレスのアクセス処理
@app.route("/")
def hello():
    return render_template("index.html", memos=data.memos)


# メモがクリックされるとここが実行される
@app.route("/receive", methods=["POST"])
def memo_clicked():
    if request.headers['Content-Type'] != 'application/json':
            print(request.headers['Content-Type'])
            return "ERROR"
            
    TYPE = {"new": 1, "edit": 2, "remove": 3}
    js = request.json
    if js["type"] == TYPE["new"]:
        data.add(js["text"])

    elif js["type"] == TYPE["edit"]:
        print("edit")

    elif js["type"] == TYPE["remove"]:
        data.remove(js["id"])
        
    print(js)
    return jsonify(res="ok")


if __name__ == "__main__":
    # flask 実行
    app.run(host="127.0.0.1", port=8080, debug=True)
