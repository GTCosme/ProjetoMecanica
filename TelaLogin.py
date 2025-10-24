import sqlite3
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
        self.login_entry = tk.Entry(self, width=40)
        self.login_entry.pack(pady=5)

        tk.Label(self, text="Senha:").pack()
        self.senha_entry = tk.Entry(self, show="*", width=40)
        self.senha_entry.pack(pady=5)

        tk.Button(self, text="Entrar", command=self.verificar_login, bg="#007bff", fg="white", width=15).pack(pady=20)

    def verificar_login(self):
        login = self.login_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha usuário e senha!")
            return

        try:

            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()


            cursor.execute("""
                SELECT * FROM funcionarios
                WHERE login = ? AND senha = ?
            """, (login, senha))

            resultado = cursor.fetchone()  # retorna None se não achar

            conexao.close()

            if resultado:
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.destroy()
                TelaPrincipal()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro de banco", f"Ocorreu um erro: {erro}")



