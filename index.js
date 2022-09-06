// Electron 初期設定
const Type = {f_open:5, f_new: 6};
const {PythonShell} = require('python-shell');
const express = require("express");
const server = express();
const bodyParser = require('body-parser');
const electron = require('electron');
const { dialog } = require('electron')
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
let mainWindow;

// ウィンドウを閉じたら修了
app.on('window-all-closed', function() {
  app.quit();
});

// 起動後処理
app.on('ready', function() {
  // Python 実行
  PythonShell.run('./app.py', null, function (err, result) {  // exe:'./resources/app/app.py'    edit: './app.py'
    if (err) throw err;
    console.log(result);
  });

  const rp = require('request-promise');
  const addr = 'http://127.0.0.1:8080'; // アドレス

  const openWindow = function() {
    mainWindow = new BrowserWindow({width: 1280, height: 720 });
    mainWindow.loadURL(addr);

    // 開発ツール
    mainWindow.webContents.openDevTools();

    // 終了したとき
    mainWindow.on('closed', function() {

      // クリアキャッシュ
      electron.session.defaultSession.clearCache(() => {})
      mainWindow = null;
    });
  };

  // HTMLクライアント作成
  const startUp = function() {
    rp(addr)
      .then(function(htmlString) {
        console.log('server started');
        openWindow();
      })
      .catch(function(err) {
        startUp();
      });
  };

  startUp();
});



// HTTP GET を受け取る
// ファイルを選択・新規作成の処理
server.use(bodyParser.urlencoded({ extended: false }));
server.use(bodyParser.json());
server.listen(8081, function() {});
server.get('/electron', function(req, res) {    
    switch(req.body["type"]) {
        // ファイル選択ダイアログ
        case Type["f_open"]: 
            url = dialog.showOpenDialogSync({
                title: "メモファイルを開く",
                defaultPath: req.body["url"],
                filters: [{name: 'メモファイル', extensions: ['ids']}],
                properties: ['openFile']
            });
            if(url) res.send(url[0])
            break;

        // ファイル新規作成ダイアログ
        case Type["f_new"]: 
            url = dialog.showSaveDialogSync({
                title: "新規メモファイル",
                defaultPath: req.body["url"],
                filters: [{name: 'メモファイル', extensions: ['ids']}],
                properties: ['createDirectory']
            });
            if(url) res.send(url);
            break;
    }
});