// Electron 初期設定
const {PythonShell} = require('python-shell');
const electron = require('electron');
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
  const addr = 'http://localhost:5000'; // アドレス

  const openWindow = function() {
    mainWindow = new BrowserWindow({width: 1280, height: 600 });
    mainWindow.loadURL(addr);

    // 開発ツール
    // mainWindow.webContents.openDevTools();

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