import sqlite3


class History:

    con = sqlite3.connect('BlackBot.db')
    cur = con.cursor()

    def __init__(self, user_ID):
        self.user_ID = user_ID

    def isUserDatebase(self):
        data = self.cur.execute('SELECT * FROM Info')
        for i in data.fetchall():
            if self.user_ID == i[0]:
                return True
        return False

    def read_name_card(self):
        name_card = self.cur.execute(f'SELECT name_card FROM Info WHERE user_id = {self.user_ID}').fetchall()[:5]
        return name_card

    def read_card(self):
        card_text = self.cur.execute(f'SELECT your_card FROM Info WHERE user_id = {self.user_ID}').fetchall()[:5]
        return card_text


class History_love:

    con = sqlite3.connect('BlackBot.db')
    cur = con.cursor()

    def __init__(self, user_ID):
        self.user_ID = user_ID

    def isUserDatebase(self):
        data = self.cur.execute('SELECT * FROM love_card')
        for i in data.fetchall():
            if self.user_ID == i[0]:
                return True
        return False

    def read_name_card_love(self):
        name_card = self.cur.execute(f'SELECT name_card_love FROM love_card WHERE user_id = {self.user_ID}').fetchall()[:5]
        return name_card

    def read_card_love(self):
        card_text = self.cur.execute(f'SELECT text_card_love FROM love_card WHERE user_id = {self.user_ID}').fetchall()[:5]
        return card_text