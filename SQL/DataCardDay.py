import sqlite3


class CardDay:

    con = sqlite3.connect('BlackBot.db')
    cur = con.cursor()

    def __init__(self, user_id, name_card, full_time):
        self.user_id = user_id
        self.name_card = name_card
        self.full_time = full_time
        try:
            self.cur.execute("CREATE TABLE card_day(user_id, name_card, full_time)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def recorde_in_date(self):
        self.cur.execute(f'INSERT INTO card_day VALUES (?, ?, ?)', (self.user_id, self.name_card, self.full_time))
        self.con.commit()