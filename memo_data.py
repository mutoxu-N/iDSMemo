import joblib, os

class MemoData():
    def __init__(self) -> None:
        if os.path.exists('memo'):
            self.memos = joblib.load("memo")
        else:
            self.memos = []

    def save(self) -> None:
        joblib.dump(self.memos, "memo", compress=3)

    def add(self, txt) -> None:
        self.memos.append(txt)
        self.save()
        
    def remove(self, idx: int) -> None:
        self.memos[idx:idx+1] = []
        self.save()
