from __future__ import print_function
import time
from flask import Flask, render_template

app = Flask(__name__)

# root アドレスのアクセス処理
@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == "__main__":
    print('on hello')
    # flask 実行
    app.run(host="127.0.0.1", port=8080)
