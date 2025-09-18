import tkinter as tk
from tkinter import ttk, messagebox
from main import Database
from chat_window import ChatWindow

class ChatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat App")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")

        self.db = Database()
        self.current_user = None

        self.setup_styles()
        self.show_login()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Dark.TFrame", background="#1e1e1e")
        style.configure("Dark.TButton",
                        background="#333333",
                        foreground="#ffffff",
                        padding=10,
                        font=('Helvetica', 10))
        style.map("Dark.TButton",
                  background=[('active', '#555555')])
        style.configure("Dark.TEntry",
                        fieldbackground="#333333",
                        foreground="#ffffff",
                        padding=5)
        style.configure("Dark.TLabel",
                        background="#1e1e1e",
                        foreground="#ffffff",
                        font=('Helvetica', 10))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        frame = ttk.Frame(self.root, style="Dark.TFrame")
        frame.pack(expand=True)

        ttk.Label(frame,
                  text="Login",
                  style="Dark.TLabel",
                  font=('Helvetica', 20)).pack(pady=20)

        self.login_username = ttk.Entry(frame, style="Dark.TEntry")
        self.login_username.pack(pady=10)

        self.login_password = ttk.Entry(frame, style="Dark.TEntry", show="*")
        self.login_password.pack(pady=10)

        ttk.Button(frame,
                   text="Login",
                   style="Dark.TButton",
                   command=self.login).pack(pady=5)

        ttk.Button(frame,
                   text="Vai a Registrazione",
                   style="Dark.TButton",
                   command=self.show_register).pack(pady=5)

    def show_register(self):
        self.clear_window()
        frame = ttk.Frame(self.root, style="Dark.TFrame")
        frame.pack(expand=True)

        ttk.Label(frame,
                  text="Registrazione",
                  style="Dark.TLabel",
                  font=('Helvetica', 20)).pack(pady=20)

        self.reg_username = ttk.Entry(frame, style="Dark.TEntry")
        self.reg_username.pack(pady=10)

        self.reg_password = ttk.Entry(frame, style="Dark.TEntry", show="*")
        self.reg_password.pack(pady=10)

        ttk.Button(frame,
                   text="Registrati",
                   style="Dark.TButton",
                   command=self.register).pack(pady=5)

        ttk.Button(frame,
                   text="Vai a Login",
                   style="Dark.TButton",
                   command=self.show_login).pack(pady=5)

    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Attenzione", "Inserisci username e password")
            return

        if self.db.login_user(username, password):
            self.current_user = username
            self.show_chat()
        else:
            messagebox.showerror("Errore", "Username o password errati")

    def register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Attenzione", "Inserisci username e password")
            return

        if self.db.register_user(username, password):
            messagebox.showinfo("Successo", "Registrazione completata! Effettua il login.")
            self.show_login()
        else:
            # L'errore è gestito nel db
            pass

    def show_chat(self):
        self.clear_window()
        self.chat_window = ChatWindow(self.root, self.current_user, self.db)
        self.chat_window.window.pack(fill=tk.BOTH, expand=True)

    def on_close(self):
        self.db.close()
        self.root.destroy()
