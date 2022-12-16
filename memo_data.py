import joblib, os, uuid, spacy
from type import Type
from database import Relation

class MemoData():
    """
    メモデータを管理するクラス
    """
    def __init__(self, filename) -> None:
        self.nlp = spacy.load('ja_ginza_electra') # 形態素解析
        self.relation = Relation("test.db")

        if filename is not None:
            self.__filename = filename
            self.load(filename)
        

    def load(self, path) -> None:
        """
        ファイルからメモデータを読み込む

        Args: 
            path (str): 読み込むファイルのパス
        """
        self.__filename = path # メモデータのファイル名

        self.__process = [None for _ in [None]*32] # undo/redo環の配列
        self.__currentCursor = -1 # undo/redo環のカーソル -1のときはundo下限をundoしたとき
        self.__undoLimit = 0 # undo/redo環のUNDO限界値
        self.__redoLimit = -1 # undo/redo環のREDO限界値

        if os.path.exists(path):
            self.__data = joblib.load(path)
        else:
            self.__data = [] # [uuid, memoContents, representativeWords]


    @property
    def memo(self) -> str:
        """
        読み込まれているメモデータのタプルを返す
        """
        # print(self.__data)
        tmp = []
        for t in self.__data:
            tmp.append("".join(t[1])) # 形態素解析後のデータを結合する
        return tuple(tmp)


    @property
    def filename(self) -> str:
        """
        ファイル名を拡張子付きで返す
        """
        return self.__filename.split('\\')[-1]


    @property
    def filenameWithNoExt(self) -> str:
        """
        拡張子の付いていいないファイル名を返す
        """
        return self.filename.split('.')[0]
        

    @property
    def memoWordsList(self) -> list:
        l = []
        for a in self.__data:
            for word in a[1]:
                l.append(word)
        return l


    def save(self) -> None:
        """
        メモデータをファイルに保存する
        """
        joblib.dump(self.__data, self.filename, compress=3)

        
    def add(self, txt, prevUUID:uuid.UUID=None, log=True) -> None:
        """
        メモにデータを追加する
        
        Args: 
            txt (str): 追加するメモの内容
            txt (list): 形態素解析語のメモデータ    
            tmpUUID (uuid, optional): UUIDを指定する 指定しなければ自動で付与する
            notDo (bool, optional): undo/redo のときはFalseに設定

        """
        if prevUUID is None:
            prevUUID = uuid.uuid4()
        
        if type(txt) is list: txt = ''.join(txt)
        l, r = self.__split(txt)

        if log: # not logged when undo/redo
            self.__do(Type.NEW, prevUUID, l)
        self.__data.append([prevUUID, l, r])
        self.__wordsInSameSentence(r) # 代表単語の関連度を設定
        self.save()
        

    def remove(self, idx: int, log=True) -> None:
        """
        メモからデータを削除する

        Args:
            idx (int): 削除するデータのインデックス
            notDo (bool, optional): undo/redo のときはFalseに設定
        """
        if log: # not logged when undo/redo
            self.__do(Type.REMOVE, self.__data[idx][0], self.__data[idx][1])
        self.__data[idx:idx+1] = []
        self.save()


    def edit(self, idx: int, txt, log=True) -> None:
        """
        メモデータを編集する

        Args:
            idx (int): 編集するデータのインデックス
            txt (str): 編集後のメモの内容
            txt (list): 形態素解析語のメモデータ
            notDo (bool, optional): undo/redo のときはFalseに設定"""
        
        if type(txt) is list: txt = ''.join(txt)
        l, r = self.__split(txt)
        
        if log: # not logged when undo/redo
            self.__do(Type.EDIT, self.__data[idx][0], {"before": self.__data[idx][1], "after": l})
        self.__data[idx][1] = l
        self.__data[idx][2] = r


    def group(self, l: list) -> None:
        """
        メモのグループを設定する

        Args: 
            l (list): グループを設定するインデックス
        """
        for i1 in range(len(l)-1):
            for i2 in range(i1+1, len(l)):
                # i1 行目 と i2 行目
                words1 = self.__data[l[i1]][2]
                words2 = self.__data[l[i2]][2]
                for w1 in words1:
                    for w2 in words2:
                        if w1 != w2: # 違う単語のとき
                            r = self.relation.getRelevance(w1, w2)
                            if r:  self.relation.update(w1, w2, r + 5)
                            else:  self.relation.update(w1, w2, 5)


    def removeAll(self, log=True) -> None:
        """
        全てのメモデータを削除する
        """
        if log:
            self.__do(Type.ALL_REMOVE, None, self.__data)
        self.__data = []


    def __do(self, action: Type, uuid: uuid.UUID, content) -> None:
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
        self.__canUndo = True

        if(self.__undoLimit == self.__redoLimit and not self.__process[-1] is None):
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
        if(self.__currentCursor == -1): # UndoLimit のプロセスをundoした後
            return 

        process = self.__process[self.__currentCursor] # [uuid, action, content]

        if(self.__currentCursor == self.__undoLimit): # cannot undo
            self.__currentCursor = -1

        if process[1] == Type.NEW:
            self.remove(self.__get_idx_from_uuid(process[0]), log=False) # remove from uuid

        elif process[1] == Type.EDIT:
            self.edit(self.__get_idx_from_uuid(process[0]), 
                     process[2]["before"], log=False) # edit to before content from uuid

        elif process[1] == Type.REMOVE:
            self.add(process[2], prevUUID=process[0], log=False) # add with same uuid

        elif process[1] == Type.ALL_REMOVE:
            self.__data = process[2]

        if(not self.__currentCursor < 0):
            self.__currentCursor = self.__prev(self.__currentCursor)


    def redo(self) -> None:
        """
        redo処理を行う
        """
        if(self.__currentCursor == self.__redoLimit):
            return

        else:
            if(self.__currentCursor < 0):
                self.__currentCursor = self.__undoLimit
            else:
                self.__currentCursor = self.__next(self.__currentCursor)

        process = self.__process[self.__currentCursor] # [uuid, action, content]
        if process[1] == Type.NEW:
            self.add(process[2], prevUUID=process[0], log=False) # add with same uuid

        elif process[1] == Type.EDIT:
            self.edit(self.__get_idx_from_uuid(process[0]), 
                     process[2]["after"], log=False) # edit to before content from uuid

        elif process[1] == Type.REMOVE:
            self.remove(self.__get_idx_from_uuid(process[0]), log=False) # remove from uuid

        elif process[1] == Type.ALL_REMOVE:
            self.removeAll(log=False)


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


    def __split(self, txt: str) -> tuple:
        """
        [private] 文字列を形態素して、リストを返す

        Args: 
            txt (str): 形態素解析したい文字列
        """
        # 形態素解析
        doc = self.nlp(txt)
        l = []
        rep = []
        for sent in doc.sents:
            for token in sent:
                if len(rep) < 3 and token.pos_ not in ['ADP', 'AUX', 'SYM']:
                    rep.append(token.orth_)
                l.append(token.orth_)
        return l, rep


    def __wordsInSameSentence(self, words: list) -> None:
        """
        [private] 同一文章内の単語の関連度を設定する

        Args:
            words (list): 代表単語の配列
        """
        
        for i in range(0, len(words)-1):
            for j in range(i+1, len(words)):
                r = self.relation.getRelevance(words[i], words[j])
                if r:  self.relation.update(words[i], words[j], r + 1)
                else:  self.relation.update(words[i], words[j], 1)
        