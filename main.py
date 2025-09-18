import sqlite3
from tkinter import messagebox

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('chat_app.db')
            self.create_tables()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")

    def create_tables(self):
        try:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS friends (
                    user1 TEXT,
                    user2 TEXT,
                    PRIMARY KEY (user1, user2)
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to create tables: {e}")

    def register_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Errore", "Username già esistente")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Registration failed: {e}")
            return False

    def login_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Login failed: {e}")
            return False

    def add_friend(self, user1, user2):
        try:
            cursor = self.conn.cursor()
            # Controlla che esistano entrambi gli utenti
            cursor.execute("SELECT username FROM users WHERE username IN (?, ?)", (user1, user2))
            if len(cursor.fetchall()) != 2:
                messagebox.showerror("Errore", "Uno o entrambi gli utenti non esistono")
                return False
            # Aggiunge solo la relazione da user1 a user2 (unidirezionale)
            cursor.execute("INSERT OR IGNORE INTO friends (user1, user2) VALUES (?, ?)", (user1, user2))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add friend: {e}")
            return False

    def get_friends(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT user2 FROM friends WHERE user1 = ?", (username,))
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to get friends: {e}")
            return []

    def get_all_users(self, exclude_username=None):
        try:
            cursor = self.conn.cursor()
            if exclude_username:
                cursor.execute("SELECT username FROM users WHERE username != ?", (exclude_username,))
            else:
                cursor.execute("SELECT username FROM users")
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to get users: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    try:
        from chat_app import ChatApp

        app = ChatApp()
        app.root.mainloop()
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile avviare l'app: {e}")
