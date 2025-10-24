import sqlite3
import tkinter as tk
from tkinter import messagebox


class TelaProduto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA PRODUTO")
        self.geometry("600x500")
        self.resizable(False, False)

        tk.Label(self, text="TELA PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Produto", width=30, command=self.tela_cadastro_produto).pack(pady=5)
        tk.Button(self, text="Consultar Quantidade", width=30, command=self.tela_consultar_quantidade).pack(pady=5)
        tk.Button(self, text="Modificar Produto", width=30, command=self.tela_modificar_produto).pack(pady=5)
        tk.Button(self, text="Voltar", width=30, command=self.voltar).pack(pady=25)


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

        tk.Label(self, text="Quantidade:").pack()
        self.entry_quantidade = tk.Entry(self, width=40)
        self.entry_quantidade.pack(pady=5)

        tk.Button(self, text="Salvar", width=15, command=self.salvar).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_produto).pack(pady=5)


    def salvar(self):
        id = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        tipoProduto = self.entry_tipoProduto.get().strip()
        preco = self.entry_preco.get().strip()
        quantidade = self.entry_quantidade.get().strip() or "0"

        if not id or not nome or not tipoProduto or not preco:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO produtos (id, nome, tipoProduto, preco, quantidade)
                VALUES (?, ?, ?, ?, ?)
            """, (id, nome, tipoProduto, preco, quantidade))
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")


            for entry in [self.entry_id, self.entry_nome, self.entry_tipoProduto,
                          self.entry_preco, self.entry_quantidade]:
                entry.delete(0, tk.END)

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {erro}")


    def tela_consultar_quantidade(self):
        self.limpar_tela()
        tk.Label(self, text="CONSULTAR QUANTIDADE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Nome do Produto:").pack()
        self.entry_nome_consulta = tk.Entry(self, width=40)
        self.entry_nome_consulta.pack(pady=5)

        tk.Button(self, text="Consultar", width=15, command=self.consultar_quantidade).pack(pady=10)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_produto).pack(pady=5)

        self.label_resultado = tk.Label(self, text="", font=("Arial", 12))
        self.label_resultado.pack(pady=20)

    def consultar_quantidade(self):
        nome = self.entry_nome_consulta.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Digite o nome do produto!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT quantidade FROM produtos WHERE nome = ?", (nome,))
            resultado = cursor.fetchone()
            conexao.close()

            if resultado:
                self.label_resultado.config(text=f"Quantidade disponível: {resultado[0]}")
            else:
                self.label_resultado.config(text="Produto não encontrado.")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")


    def tela_modificar_produto(self):
        self.limpar_tela()
        tk.Label(self, text="MODIFICAR PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite o ID do Produto:").pack()
        self.entry_id_mod = tk.Entry(self, width=40)
        self.entry_id_mod.pack(pady=5)

        tk.Button(self, text="Buscar Produto", width=15, command=self.buscar_produto).pack(pady=10)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_produto).pack(pady=5)

        self.frame_edicao = tk.Frame(self)
        self.frame_edicao.pack(pady=10)

    def buscar_produto(self):
        id_prod = self.entry_id_mod.get().strip()
        if not id_prod:
            messagebox.showwarning("Atenção", "Digite o ID do produto!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, tipoProduto, preco, quantidade FROM produtos WHERE id = ?", (id_prod,))
            produto = cursor.fetchone()
            conexao.close()

            for widget in self.frame_edicao.winfo_children():
                widget.destroy()

            if produto:
                tk.Label(self.frame_edicao, text="Nome:").pack()
                self.entry_nome_mod = tk.Entry(self.frame_edicao, width=40)
                self.entry_nome_mod.pack(pady=5)
                self.entry_nome_mod.insert(0, produto[0])

                tk.Label(self.frame_edicao, text="Tipo do Produto:").pack()
                self.entry_tipo_mod = tk.Entry(self.frame_edicao, width=40)
                self.entry_tipo_mod.pack(pady=5)
                self.entry_tipo_mod.insert(0, produto[1])

                tk.Label(self.frame_edicao, text="Preço:").pack()
                self.entry_preco_mod = tk.Entry(self.frame_edicao, width=40)
                self.entry_preco_mod.pack(pady=5)
                self.entry_preco_mod.insert(0, produto[2])

                tk.Label(self.frame_edicao, text="Quantidade:").pack()
                self.entry_quantidade_mod = tk.Entry(self.frame_edicao, width=40)
                self.entry_quantidade_mod.pack(pady=5)
                self.entry_quantidade_mod.insert(0, produto[3])

                tk.Button(self.frame_edicao, text="Salvar Alterações", command=self.salvar_alteracoes).pack(pady=10)
                tk.Button(self.frame_edicao, text="Excluir Produto", command=self.excluir_produto, fg="red").pack(pady=5)

            else:
                messagebox.showinfo("Info", "Produto não encontrado!")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

    def salvar_alteracoes(self):
        id_prod = self.entry_id_mod.get().strip()
        nome = self.entry_nome_mod.get().strip()
        tipo = self.entry_tipo_mod.get().strip()
        preco = self.entry_preco_mod.get().strip()
        quantidade = self.entry_quantidade_mod.get().strip() or "0"

        if not nome or not tipo or not preco:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE produtos
                SET nome = ?, tipoProduto = ?, preco = ?, quantidade = ?
                WHERE id = ?
            """, (nome, tipo, preco, quantidade, id_prod))
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.destroy()
            from TelaPrincipal import TelaPrincipal
            TelaPrincipal().mainloop()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

    def excluir_produto(self):
        id_prod = self.entry_id_mod.get().strip()
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este produto?"):
            try:
                conexao = sqlite3.connect("mecanica_master.db")
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM produtos WHERE id = ?", (id_prod,))
                conexao.commit()
                conexao.close()

                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                self.destroy()
                from TelaPrincipal import TelaPrincipal
                TelaPrincipal().mainloop()

            except sqlite3.Error as erro:
                messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal().mainloop()

    def voltar_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto
        TelaProduto().mainloop()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()



