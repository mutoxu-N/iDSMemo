import joblib, os

class MemoConfig():
    def __init__(self):
        # __config
        # 0: opening file url
        self.__config = []
        self.load()

    def save(self) -> None:
        joblib.dump(self.__config, "config.cfg", compress=3)

    def load(self) -> None:
        if os.path.exists("config.cfg"):
            self.__config = joblib.load("config.cfg")
        else:
            self.__config = ["C:/memo.ids"]
    
    @property
    def url(self) -> str:
        self.load()
        return self.__config[0]

    @property
    def dir(self) -> str:
        self.load()
        return  '/'.join(self.url.split('/')[:-1])


    def setDir(self, url: str) -> None:
        self.__config[0] = url
        self.save()
    
