import sqlite3

class DB():
    def __init__(self):
        self.conn = sqlite3.connect('planning.db')
        self.cursor = self.conn.cursor()
        
    def add_note(self, value, d):
        self.cursor.execute(f"INSERT INTO notes (id_week, note) VALUES ('{d}', '{value}')")
        self.conn.commit()
                
    def edit_note(self, value, d):
        self.cursor.execute(f"UPDATE notes SET note = '{value}' WHERE id_week = '{d}'")
        self.conn.commit()
        
    def delete_note(self, d):
        self.cursor.execute(f"DELETE FROM notes WHERE id_week = '{d}'")
        self.conn.commit()

    def get_data(self, d1, d2):
        data_ = self.cursor.execute("SELECT * FROM week WHERE date_day BETWEEN ? AND ?", (d1, d2)).fetchall()
        return data_
    
    def is_data(self, d):
        query = self.cursor.execute(f"SELECT date_day FROM week WHERE date_day = '{d}'").fetchone()
        if (query):
            return True
        return False

    def edit_data(self, col, value, d):
        self.cursor.execute(f"UPDATE week SET {col} = '{value}' WHERE date_day = '{d}'")
        self.conn.commit()
        
    def delete_data(self, col, d):
        self.cursor.execute(f"UPDATE week SET {col} = NULL WHERE date_day = '{d}'")
        self.conn.commit()

    def add_data(self, col, d, value):
        self.cursor.execute(f"INSERT INTO week (date_day, {col}) VALUES ('{d}', '{value}')")
        self.conn.commit()

    def get_note(self, d):
        query = self.cursor.execute(f"SELECT note FROM notes WHERE id_week = '{d}'").fetchone()
        return query[0]
    
    def is_note(self, d):
        query = self.cursor.execute(f"SELECT id FROM notes WHERE id_week = '{d}'").fetchone()
        if (query):
            return True
        return False
