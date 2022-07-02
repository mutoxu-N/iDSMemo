import joblib, os
from type import Type
import uuid

class MemoData():
    def __init__(self, filename) -> None:
        self.__filename = filename
        self.load(filename)

    def load(self, filename) -> None:
        self.__filename = filename
        self.__process = [None for _ in [None]*5]
        self.__currentCursor = 0
        self.__undoLimit = 0
        self.__redoLimit = -1
        self.__canRedo = False

        if os.path.exists(filename):
            self.__data = joblib.load(filename)
        else:
            self.__data = [] # [uuid, memoContents]

    @property
    def memo(self) -> str:
        tmp = []
        for t in self.__data:
            tmp.append(t[1])
        return tuple(tmp)

    @property
    def filename(self) -> str:
        return self.__filename.split('/')[-1]
        

    def save(self) -> None:
        joblib.dump(self.__data, self.filename, compress=3)

        
    def add(self, txt, tmpUUID=None, notDo=True) -> None:
        if tmpUUID is None:
            tmpUUID = uuid.uuid4()
        if notDo: # not logged when undo/redo
            self.__do(Type.NEW, tmpUUID, txt)
        self.__data.append([tmpUUID, txt])
        self.save()
        

    def remove(self, idx: int, notDo=True) -> None:
        if notDo: # not logged when undo/redo
            self.__do(Type.REMOVE, self.__data[idx][0], self.__data[idx][1])
        self.__data[idx:idx+1] = []
        self.save()


    def edit(self, idx: int, text: str, notDo=True) -> None:
        if notDo: # not logged when undo/redo
            self.__do(Type.REMOVE, self.__data[idx][0], {"before": self.__data[idx][1], "after": text})
        self.__data[idx] = text


    def __do(self, action: Type, uuid, content):
        self.__redoLimit = self.__next(self.__currentCursor)
        self.__currentCursor = self.__redoLimit
        self.__process[self.__currentCursor] = [uuid, action, content]

        if(self.__undoLimit == self.__redoLimit and self.__process[-1]):
            self.__undoLimit = self.__next(self.__undoLimit)
            

    def __next(self, idx):
        return (idx+1) % len(self.__process)

    def __prev(self, idx):
        return (idx+len(self.__process)-1) % len(self.__process)


    def undo(self):        
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

    def redo(self):

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



    def __get_idx_from_uuid(self, uuid):
        for t in self.__data:
            if t[0] == uuid:
                return self.__data.index(t)
        return -1
