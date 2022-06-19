import joblib, os

class MemoData():
    def __init__(self) -> None:
        if os.path.exists('memo'):
            self.__memos = joblib.load("memo")
        else:
            self.__memos = []

    @property
    def memo(self):
        return tuple(self.__memos)

    def save(self) -> None:
        joblib.dump(self.__memos, "memo", compress=3)

    def add(self, txt) -> None:
        self.__memos.append(txt)
        self.save()
        
    def remove(self, idx: int) -> None:
        self.__memos[idx:idx+1] = []
        self.save()

    def set(self, id: int, text: str) -> None:
        self.__memos[id] = text
