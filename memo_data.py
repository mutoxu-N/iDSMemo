import joblib, os

class MemoData():
    def __init__(self, filename) -> None:
        self.__filename = filename
        if os.path.exists(filename):
            self.__memos = joblib.load(filename)
        else:
            self.__memos = []

    @property
    def memo(self) -> str:
        return tuple(self.__memos)

    @property
    def filename(self) -> str:
        return self.__filename

    def save(self) -> None:
        joblib.dump(self.__memos, self.filename, compress=3)

    def add(self, txt) -> None:
        self.__memos.append(txt)
        self.save()
        
    def remove(self, idx: int) -> None:
        self.__memos[idx:idx+1] = []
        self.save()

    def set(self, id: int, text: str) -> None:
        self.__memos[id] = text
