import sqlite3
import datetime

class UserQueue:
    def __init__(self):
        self.conn = sqlite3.connect("/home/cplalexandtang/summerbot/api/db/db.sqlite3")
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

def getNewNumber():
    pass

if __name__ == '__main__':
    u1 = UserQueue()
    u1.push("U123", "Alex")