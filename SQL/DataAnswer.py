import sqlite3


class Questions:

    con = sqlite3.connect('BlackBot.db')
    cur = con.cursor()

    def __init__(self, user_id, full_name_users, your_card, name_card):
        self.user_id = user_id
        self.full_name_users = full_name_users
        self.your_card = your_card
        self.name_card = name_card
        try:
            self.cur.execute("CREATE TABLE Info(user_id, full_name_users, your_card, name_card)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def recorde_in_data(self):
        self.cur.execute(f'INSERT INTO Info VALUES (?, ?, ?, ?)', (self.user_id, self.full_name_users, self.your_card, self.name_card))
        self.con.commit()


class add_wisdoms:

    con = sqlite3.connect('BlackBot.db')
    cur = con.cursor()

    def __init__(self, user_id, full_name_user, add_wisdom):
        self.user_id = user_id
        self.full_name_user = full_name_user
        self.add_wisdom = add_wisdom
        try:
            self.cur.execute("CREATE TABLE wisdom(user_id, full_name_user, wisdoms)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def write_wisdoms(self):
        self.cur.execute(f'INSERT INTO wisdom VALUES (?, ?, ?)', (self.user_id, self.full_name_user, self.add_wisdom))
        self.con.commit()


class card_love:

    con = sqlite3.connect('BlackBot.db')
    cur = con.cursor()

    def __init__(self, user_id, full_name_user, name_card_love, text_card_love):
        self.user_id = user_id
        self.full_name_user = full_name_user
        self.name_card_love = name_card_love
        self.text_card_love = text_card_love
        try:
            self.cur.execute("CREATE TABLE love_card(user_id, full_name_user, name_card_love, text_card_love)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def write(self):
        self.cur.execute(f'INSERT INTO love_card VALUES (?, ?, ?, ?)', (self.user_id, self.full_name_user, self.name_card_love, self.text_card_love))
        self.con.commit()

