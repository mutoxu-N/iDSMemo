from __future__ import print_function
from crypt import methods
from flask import Flask, render_template, request
import memo_data

app = Flask(__name__)
data = memo_data.MemoData()

# root アドレスのアクセス処理
@app.route("/")
def hello():
    return render_template("index.html")

def memo_clicked():
    print('pong')


# TODO JavaScriptからPython関数を実行する
@app.route("/test/", methods=['GET'])
def test():
    print(request.args.get('a'))


if __name__ == "__main__":
    print('on hello')
    # flask 実行
    app.run(host="127.0.0.1", port=8080)
