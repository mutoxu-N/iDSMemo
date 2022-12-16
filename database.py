import sqlite3, hashlib, os

class Relation():
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.conn = None
    

    def getRelevance(self, w1: str, w2: str) -> float:
        """
        DBから関連度を取得する

        Args:
            w1 (str): 単語1
            w2 (str): 単語2
        """
        self.__connect()
        cursor = self.conn.cursor()
        h = self.__hashFormat(w1, w2)
        sql = f"select * from Words where W1=\"{h[0]}\" and W2=\"{h[1]}\";"
        cursor.execute(sql)

        res = cursor.fetchone()
        cursor.close()

        ret = None
        if res:  ret = float(res[2])
        self.__close()
        return ret
        

    def update(self, w1: str, w2: str, r: float) -> None:
        """
        単語の関連度を更新する。

        Args:
            w1 (str): 単語1
            w2 (str): 単語2
            r (float): 設定する関連度
        """
        self.__connect()
        cursor = self.conn.cursor()
        h = self.__hashFormat(w1, w2)
        sql = f"select * from Words where W1=\"{h[0]}\" and W2=\"{h[1]}\";"
        cursor.execute(sql)

        res = cursor.fetchone() # tuple(W1, W2, R)

        if res:
            sql = f"delete from Words where W1=\"{h[0]}\" and W2=\"{h[1]}\";"
            cursor.execute(sql)
        
        self.insert(w1, w2, r)
        
        cursor.close()
        self.conn.commit()
        self.__close()
    

    def insert(self, w1: str, w2:str, r:float =0) -> None:
        """
        単語同士の関連度をDBに追加する。

        Args:
            w1 (str): 単語1
            w2 (str): 単語2
            r (float): 設定する関連度 (初期値=0)
        """

        self.__connect()
        cursor = self.conn.cursor()
        h = self.__hashFormat(w1, w2)
        sql = f"insert into Words(W1, W2, R) values(\"{h[0]}\", \"{h[1]}\", {r});"
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()
        self.__close()

    
    def __hashFormat(self, w1:str, w2: str) -> tuple:
        """
        [private] テキストからハッシュ値の組(ハッシュの順)を返す。

        Args:
            w1 (str): 単語1
            w2 (str): 単語2
        """

        h1 = hashlib.sha256(w1.encode()).hexdigest()
        h2 = hashlib.sha256(w2.encode()).hexdigest()
        return (min(h1, h2), max(h1, h2))


    def createDatabase(self) -> None:
        """
        DBテーブルを作成する。
        """
        self.__connect()
        cursor = self.conn.cursor()
        cursor.execute("create table Words(W1 nchar(64) , W2 nchar(64), R double, primary key(W1, W2));")
        self.conn.commit()
        self.__close()


    def __connect(self) -> None:
        """
        データベースに接続する。
        """
        if not os.path.exists(self.filename): self.createDatabase()
        self.conn = sqlite3.connect(self.filename)


    def __close(self):
        """
        データベースへの接続を解除する
        """
        self.conn.close()
        self.conn = None
        



if __name__ == '__main__':
    a = Relation()
    # a.insert("こんにちは", "オレンジ")
    print(a.getRelevance("オレンジ", "こんにちは"))
    a.update("こんにちは", "オレンジ", 5)
    print(a.getRelevance("オレンジ", "こんにちは"))