import tkinter as tk
from tkinter import messagebox
from TelaPrincipal import TelaPrincipal

class TelaLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA LOGIN")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA LOGIN", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self, text="Usuário:").pack()
        self.usuario_entry = tk.Entry(self, width=40)
        self.usuario_entry.pack(pady=5)

        tk.Label(self, text="Senha:").pack()
        self.senha_entry = tk.Entry(self, show="*", width=40)
        self.senha_entry.pack(pady=5)

        tk.Button(self, text="Entrar", command=self.verificar_login, bg="#007bff", fg="white", width=15).pack(pady=20)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        if usuario == "flavio" and senha == "1234":
            self.destroy()
            TelaPrincipal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
