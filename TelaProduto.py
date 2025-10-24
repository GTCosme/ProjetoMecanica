import sqlite3
import tkinter as tk
from tkinter import messagebox


class TelaProduto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA PRODUTO")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Produto", width=30, command=self.tela_cadastro_produto).pack(pady=5)
        tk.Button(self, text="Consultar Quantidade", width=30).pack(pady=5)
        tk.Button(self, text="Modificar Produto", width=30).pack(pady=5)
        tk.Button(self, text="Voltar", width=30, command=self.voltar).pack(pady=25)

        self.mainloop()

    def tela_cadastro_produto(self):
        self.limpar_tela()
        tk.Label(self, text="TELA CADASTRO PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="ID:").pack()
        self.entry_id = tk.Entry(self, width=40)
        self.entry_id.pack(pady=5)

        tk.Label(self, text="Nome do Produto:").pack()
        self.entry_nome = tk.Entry(self, width=40)
        self.entry_nome.pack(pady=5)

        tk.Label(self, text="Tipo do Produto:").pack()
        self.entry_tipoProduto = tk.Entry(self, width=40)
        self.entry_tipoProduto.pack(pady=5)

        tk.Label(self, text="Preço:").pack()
        self.entry_preco = tk.Entry(self, width=40)
        self.entry_preco.pack(pady=5)

        tk.Button(self, text="Salvar", width=15, command=self.salvar).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_produto).pack()

    def salvar(self):
        id = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        tipoProduto = self.entry_tipoProduto.get().strip()
        preco = self.entry_preco.get().strip()

        if not id or not nome or not tipoProduto or not preco:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO produtos (id, nome, tipoProduto, preco)
                VALUES (?, ?, ?, ?)
            """, (id, nome, tipoProduto, preco))

            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

            # 🔹 Limpar campos após salvar
            self.entry_id.delete(0, tk.END)
            self.entry_nome.delete(0, tk.END)
            self.entry_tipoProduto.delete(0, tk.END)
            self.entry_preco.delete(0, tk.END)

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {erro}")

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def voltar_produto(self):
        self.destroy()
        TelaProduto()
