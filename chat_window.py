import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ChatWindow:
    def __init__(self, parent, username, db):
        self.window = ttk.Frame(parent, style="Dark.TFrame")
        self.username = username
        self.db = db

        self.setup_chat_interface()
        self.refresh_friends_list()

    def setup_chat_interface(self):
        # Left panel - Friends list and add friend
        left_panel = ttk.Frame(self.window, style="Dark.TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(left_panel,
                  text=f"Benvenuto, {self.username}",
                  style="Dark.TLabel",
                  font=('Helvetica', 14, 'bold')).pack(pady=10)

        ttk.Button(left_panel,
                   text="Aggiungi Amico",
                   style="Dark.TButton",
                   command=self.add_friend_dialog).pack(pady=5)

        self.friends_list = tk.Listbox(left_panel,
                                      bg="#333333",
                                      fg="#ffffff",
                                      selectmode=tk.SINGLE,
                                      height=20)
        self.friends_list.pack(fill=tk.BOTH, expand=True, pady=5)

        # Chat area (per ora solo placeholder)
        chat_area = ttk.Frame(self.window, style="Dark.TFrame")
        chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.messages_text = tk.Text(chat_area,
                                     bg="#333333",
                                     fg="#ffffff",
                                     wrap=tk.WORD,
                                     state=tk.DISABLED)
        self.messages_text.pack(fill=tk.BOTH, expand=True, pady=5)

        input_frame = ttk.Frame(chat_area, style="Dark.TFrame")
        input_frame.pack(fill=tk.X, pady=5)

        self.message_entry = ttk.Entry(input_frame, style="Dark.TEntry")
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(input_frame,
                   text="Invia",
                   style="Dark.TButton",
                   command=self.send_message).pack(side=tk.LEFT, padx=5)

    def refresh_friends_list(self):
        self.friends_list.delete(0, tk.END)
        friends = self.db.get_friends(self.username)
        if friends:
            for friend in friends:
                self.friends_list.insert(tk.END, friend)
        else:
            self.friends_list.insert(tk.END, "Nessun amico aggiunto")

    def add_friend_dialog(self):
        username_to_add = simpledialog.askstring("Aggiungi Amico", "Inserisci username da aggiungere:")
        if username_to_add:
            username_to_add = username_to_add.strip()
            if username_to_add == self.username:
                messagebox.showerror("Errore", "Non puoi aggiungere te stesso")
                return

            all_users = self.db.get_all_users(exclude_username=self.username)
            if username_to_add not in all_users:
                messagebox.showerror("Errore", "Utente non trovato")
                return

            if username_to_add in self.db.get_friends(self.username):
                messagebox.showinfo("Info", "Utente già presente nella tua lista amici")
                return

            if self.db.add_friend(self.username, username_to_add):
                messagebox.showinfo("Successo", f"{username_to_add} aggiunto come amico")
                self.refresh_friends_list()
            else:
                messagebox.showerror("Errore", "Impossibile aggiungere amico")

    def send_message(self):
        msg = self.message_entry.get().strip()
        if not msg:
            return
        self.messages_text.configure(state=tk.NORMAL)
        self.messages_text.insert(tk.END, f"\n{self.username}: {msg}")
        self.messages_text.configure(state=tk.DISABLED)
        self.message_entry.delete(0, tk.END)
