import sqlite3
import tkinter as tk
from tkinter import messagebox


class TelaCliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA CLIENTE")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Cliente", width=30, command=self.tela_cadastro_cliente).pack(pady=5)
        tk.Button(self, text="Consultar Cliente", width=30).pack(pady=5)
        tk.Button(self, text="Modificar Cliente", width=30).pack(pady=5)
        tk.Button(self, text="Voltar", width=30, command=self.voltar).pack(pady=25)

        self.mainloop()

    def tela_cadastro_cliente(self):
        self.limpar_tela()

        tk.Label(self, text="TELA CADASTRO CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Nome do Cliente:").pack()
        self.entry_nome = tk.Entry(self, width=40)
        self.entry_nome.pack(pady=5)

        tk.Label(self, text="CPF:").pack()
        self.entry_cpf = tk.Entry(self, width=40)
        self.entry_cpf.pack(pady=5)

        tk.Label(self, text="Telefone:").pack()
        self.entry_telefone = tk.Entry(self, width=40)
        self.entry_telefone.pack(pady=5)

        tk.Label(self, text="Email:").pack()
        self.entry_email = tk.Entry(self, width=40)
        self.entry_email.pack(pady=5)

        tk.Button(self, text="Salvar", width=15, command=self.salvar).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_cliente).pack()

    def salvar(self):
        cpf = self.entry_cpf.get().strip()
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        if not cpf or not nome or not email or not telefone:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO clientes (cpf, nome, email, telefone)
                VALUES (?, ?, ?, ?)
            """, (cpf, nome, email, telefone))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.entry_cpf.delete(0, tk.END)
            self.entry_nome.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_telefone.delete(0, tk.END)
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {erro}")

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def voltar_cliente(self):
        self.destroy()
        TelaCliente()
