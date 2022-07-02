import joblib, os
from type import Type
import uuid

class MemoData():
    """
    メモデータを管理するクラス
    """
    def __init__(self, filename) -> None:
        self.__filename = filename
        self.load(filename)

    def load(self, path) -> None:
        """
        ファイルからメモデータを読み込む

        Args: 
            path (str): 読み込むファイルのパス
        """
        self.__filename = path # メモデータのファイル名

        self.__process = [None for _ in [None]*5] # undo/redo環の配列
        self.__currentCursor = 0 # undo/redo環のカーソル
        self.__undoLimit = 0 # undo/redo環のUNDO限界値
        self.__redoLimit = -1 # undo/redo環のREDO限界値
        self.__canRedo = False # undo/redo環でのredo可否

        if os.path.exists(path):
            self.__data = joblib.load(path)
        else:
            self.__data = [] # [uuid, memoContents]

    @property
    def memo(self) -> str:
        """
        読み込まれているメモデータのタプルを返す
        """
        tmp = []
        for t in self.__data:
            tmp.append(t[1])
        return tuple(tmp)

    @property
    def filename(self) -> str:
        """
        ファイル名を拡張子付きで返す
        """
        return self.__filename.split('/')[-1]
        

    def save(self) -> None:
        """
        メモデータをファイルに保存する
        """
        joblib.dump(self.__data, self.filename, compress=3)

        
    def add(self, txt, tmpUUID=None, notDo=True) -> None:
        """
        メモにデータを追加する
        
        Args: 
            txt (str): 追加するメモの内容
            tmpUUID (uuid, optional): UUIDを指定する 指定しなければ自動で付与する
            notDo (bool, optional): undo/redo のときはFalseに設定

        """
        if tmpUUID is None:
            tmpUUID = uuid.uuid4()
        if notDo: # not logged when undo/redo
            self.__do(Type.NEW, tmpUUID, txt)
        self.__data.append([tmpUUID, txt])
        self.save()
        

    def remove(self, idx: int, notDo=True) -> None:
        """
        メモからデータを削除する

        Args:
            idx (int): 削除するデータのインデックス
            notDo (bool, optional): undo/redo のときはFalseに設定
        """
        if notDo: # not logged when undo/redo
            self.__do(Type.REMOVE, self.__data[idx][0], self.__data[idx][1])
        self.__data[idx:idx+1] = []
        self.save()


    def edit(self, idx: int, txt: str, notDo=True) -> None:
        """
        メモデータを編集する

        Args:
            idx (int): 編集するデータのインデックス
            txt (str): 編集後のメモの内容
            notDo (bool, optional): undo/redo のときはFalseに設定"""
        if notDo: # not logged when undo/redo
            self.__do(Type.REMOVE, self.__data[idx][0], {"before": self.__data[idx][1], "after": txt})
        self.__data[idx] = txt


    def __do(self, action: Type, uuid, content) -> None:
        """
        [private] データ変更があったときに実行される
        undo/redo 処理のために履歴を登録する

        Args:
            action (Type): 実行した操作の種類
            uuid (uuid): 対象のメモのUUID
            content (object): 操作に対応した内容

        Examples:
            >> self.__do(Type.ADD, "abcde")
            >> self.__do(Type.EDIT, self.__memoData[0][0], {"before": self.__data[idx][1], "after": txt})
            >> self.__do(Type.REMOVE, 3)

        """
        self.__redoLimit = self.__next(self.__currentCursor)
        self.__currentCursor = self.__redoLimit
        self.__process[self.__currentCursor] = [uuid, action, content]

        if(self.__undoLimit == self.__redoLimit and self.__process[-1]):
            self.__undoLimit = self.__next(self.__undoLimit)


    def __next(self, idx) -> None:
        """
        [private] 入力されたインデックスの次のインデックスを取得

        Args:
            idx (int): 基準となるインデックス
        """
        return (idx+1) % len(self.__process)


    def __prev(self, idx) -> None:
        """
        [private] 入力されたインデックスの前のインデックスを取得

        Args:
            idx (int): 基準となるインデックス
        """
        return (idx+len(self.__process)-1) % len(self.__process)


    def undo(self) -> None:
        """
        undo処理を行う
        """
        if(self.__currentCursor == self.__undoLimit): # cannot undo
            return

        pos = self.__currentCursor
        if self.__process[pos][1] == Type.NEW:
            self.remove(self.__get_idx_from_uuid(self.__process[pos][0]), notDo=False) # remove from uuid

        elif self.__process[pos][1] == Type.EDIT:
            self.set(self.__get_idx_from_uuid(self.__process[pos][0]), 
                     self.__process[pos][2]["before"], notDo=False) # edit to before content from uuid

        elif self.__process[pos][1] == Type.REMOVE:
            self.add(self.__process[pos][2], tmpUUID=self.__process[pos][0], notDo=False) # add with same uuid

        self.__canRedo = True
        self.__currentCursor = self.__prev(pos)


    def redo(self) -> None:
        """
        redo処理を行う
        """
        if(self.__currentCursor == self.__redoLimit):
            self.__canRedo = False
        else:
            self.__currentCursor = self.__next(self.__currentCursor)

        pos = self.__currentCursor
        if(not self.__canRedo): # cannot redo
            return


        if self.__process[pos][1] == Type.NEW:
            self.add(self.__process[pos][2], tmpUUID=self.__process[pos][0], notDo=False) # add with same uuid

        elif self.__process[pos][1] == Type.EDIT:
            self.set(self.__get_idx_from_uuid(self.__process[pos][0]), 
                     self.__process[pos][2]["after"], notDo=False) # edit to before content from uuid

        elif self.__process[pos][1] == Type.REMOVE:
            self.remove(self.__get_idx_from_uuid(self.__process[pos][0]), notDo=False) # remove from uuid


    def __get_idx_from_uuid(self, uuid) -> int:
        """
        [private] UUIDからメモのインデックスを取得する

        Args:
            uuid (uuid): 基準となるUUID
        """
        for t in self.__data:
            if t[0] == uuid:
                return self.__data.index(t)
        return -1
