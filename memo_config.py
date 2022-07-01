import joblib, os

class MemoConfig():
    def __init__(self):
        # __config
        # 0: opening file  1:file open url
        self.__config = []
        self.load()

    def save(self) -> None:
        joblib.dump(self.__config, "config.cfg", compress=3)

    def load(self) -> None:
        if os.path.exists("config.cfg"):
            self.__config = joblib.load("config.cfg")
        else:
            self.__config = ["memo.ids", "C:"]
    
    @property
    def filename(self) -> str:
        self.load()
        return self.__config[0]

    @property
    def dirname(self) -> str:
        self.load()
        return self.__config[1]

    def setFilename(self, name: str) -> None:
        self.__config[0] = name
        self.save()

    def setDir(self, url: str) -> None:
        self.__config[1] = url
        self.save()
    
