import joblib, os

class MemoConfig():
    """
    このアプリの設定を管理するクラス
    """
    def __init__(self) -> None:
        self.__config = [] # config 0:filepath
        self.load() 

    @property
    def url(self) -> str:
        """
        最後に開いたファイルのパスを返す
        """
        self.load()
        return self.__config[0]

    @property
    def dir(self) -> str:
        """
        最後に開いたファイルのフォルダパスを返す
        """
        self.load()
        return  '/'.join(self.url.split('/')[:-1])


    def save(self) -> None:
        """
        現在のメモデータをファイルに書き込む
        """
        joblib.dump(self.__config, "config.cfg", compress=3)


    def load(self) -> None:
        """
        ファイルからメモデータを読み込む
        """
        if os.path.exists("config.cfg"):
            self.__config = joblib.load("config.cfg")
        else:
            self.__config = ["C:/memo.ids"]
            self.save()
    

    def setDir(self, url: str) -> None:
        """
        ファイルパスを設定する

        Args:
            url (str): 設定したいファイルパス
        """
        if os.path.exists(url):
            self.__config[0] = url
            self.save()
        else:
            joblib.dump([], url, compress=3)
    