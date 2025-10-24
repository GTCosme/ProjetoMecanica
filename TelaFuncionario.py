import tkinter as tk
from tkinter import messagebox
import sqlite3

class TelaFuncionario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA FUNCIONÁRIO")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Funcionário", width=30, command=self.tela_cadastro_funcionario).pack(pady=5)
        tk.Button(self, text="Modificar Funcionário", width=30).pack(pady=5)
        tk.Button(self, text="Voltar", width=30, command=self.voltar).pack(pady=25)

        self.mainloop()

    def tela_cadastro_funcionario(self):
        self.limpar_tela()

        tk.Label(self, text="TELA CADASTRO FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Nome do Funcionário:").pack()
        self.entry_nome = tk.Entry(self, width=40)
        self.entry_nome.pack(pady=5)

        tk.Label(self, text="CPF:").pack()
        self.entry_cpf = tk.Entry(self, width=40)
        self.entry_cpf.pack(pady=5)

        tk.Label(self, text="Login:").pack()
        self.entry_login = tk.Entry(self, width=40)
        self.entry_login.pack(pady=5)

        tk.Label(self, text="Senha:").pack()
        self.entry_senha = tk.Entry(self, width=40, show="*")
        self.entry_senha.pack(pady=5)

        tk.Button(self, text="Salvar", width=15, command=self.salvar).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_funcionario).pack()

    def salvar(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        login = self.entry_login.get()
        senha = self.entry_senha.get()

        if not nome or not cpf or not login or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")  # <-- troque pelo nome real do seu banco
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO funcionarios (cpf, nome, login, senha)
                VALUES (?, ?, ?, ?)
            """, (cpf, nome, login, senha))

            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            self.entry_cpf.delete(0,tk.END)
            self.entry_nome.delete(0,tk.END)
            self.entry_login.delete(0,tk.END)
            self.entry_senha.delete(0,tk.END)


        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {erro}")

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def voltar_funcionario(self):
        self.destroy()
        TelaFuncionario()
