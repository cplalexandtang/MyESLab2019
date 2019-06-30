import sqlite3
import datetime

class UserQueue:
    def __init__(self):
        self.conn = sqlite3.connect("C:/Users/cplalexandtang/Desktop/MyESLab2019/Final/backend/api/db/db.sqlite3")
        self.cur = self.conn.cursor()
    
    def tail(self):
        self.cur.execute("SELECT number FROM users_in_line ORDER BY number DESC")
        res = self.cur.fetchall()
        if len(res):
            last = res[0][0]
        else: last = 0
        
        return last
    
    def push(self, uuid, name):
        last = self.tail()
        now = last + 1

        data = ("'" + uuid + "', ") + ("'" + name + "', ") + (str(now) + ", ") + ("'" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'")
        self.cur.execute("INSERT INTO users_in_line VALUES ( " + data + ")")
        self.conn.commit()

        return now

    def waitingList(self):
        self.cur.execute("SELECT number FROM users_in_line ORDER BY number ASC")
        res = self.cur.fetchall()
        for i in range(len(res)):
            res[i] = res[i][0]
        return res

    def pop(self, uuid = None, number = None):
        if uuid:
            self.cur.execute("DELETE FROM users_in_line WHERE uuid = '" + uuid + "'")
        elif number:
            self.cur.execute("DELETE FROM users_in_line WHERE number = '" + number + "'")
        self.conn.commit()

        return "OK"

    def getId(self, number):
        self.cur.execute("SELECT uuid FROM users_in_line WHERE number = '" +  number + "'")
        res = self.cur.fetchall()
        if len(res):
            return res[0][0]
        else:
            return -1

if __name__ == '__main__':
    u1 = UserQueue()
    u1.push("U123", "Alex")