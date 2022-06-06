from __future__ import print_function
from flask import Flask, render_template, request
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
            
    TYPE = {"new": 1, "edit": 2}
    js = request.json
    if js["type"] == TYPE["new"]:
        print("new")
    elif js["type"] == TYPE["edit"]:
        print("edit")
    print(request.json)
    return ""


if __name__ == "__main__":
    # flask 実行
    app.run(host="127.0.0.1", port=8080, debug=True)
