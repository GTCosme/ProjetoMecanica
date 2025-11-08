import sqlite3
import tkinter as tk
from tkinter import messagebox
from Metodos import Metodos

# =================== TELA PRINCIPAL PRODUTO ===================
class TelaProduto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA PRODUTO")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Produto", width=25, command=self.abrir_cadastro).pack(pady=5)
        tk.Button(self, text="Consultar Quantidade", width=25, command=self.abrir_consultar).pack(pady=5)
        tk.Button(self, text="Modificar Produto", width=25, command=self.abrir_modificar).pack(pady=5)
        tk.Button(self, text="Excluir Produto", width=25, fg="red", command=self.abrir_excluir).pack(pady=5)
        tk.Button(self, text="Voltar", width=25, command=self.voltar).pack(pady=20)

        self.mainloop()

    def abrir_cadastro(self):
        self.destroy()
        CadastroProduto()

    def abrir_consultar(self):
        self.destroy()
        ConsultarProduto()

    def abrir_modificar(self):
        self.destroy()
        ModificarProduto()

    def abrir_excluir(self):
        self.destroy()
        ExcluirProduto()

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()

# =================== CADASTRO PRODUTO ===================
class CadastroProduto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastrar Produto")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA CADASTRO PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        self.entry_id = Metodos.criar_entry(self, "ID:")
        self.entry_nome = Metodos.criar_entry(self, "Nome do Produto:")
        self.entry_tipo = Metodos.criar_entry(self, "Tipo do Produto:")
        self.entry_preco = Metodos.criar_entry(self, "Preço:")
        self.entry_preco.bind("<FocusOut>", lambda e: Metodos.formatar_moeda(self.entry_preco))
        self.entry_quantidade = Metodos.criar_entry(self, "Quantidade:")

        tk.Button(self, text="Salvar", width=15, command=self.salvar).pack(pady=10)
        tk.Button(self, text="Voltar", width=15, command=self.voltar).pack(pady=5)

        self.mainloop()

    def salvar(self):
        id = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        tipo = self.entry_tipo.get().strip()
        preco = self.entry_preco.get().strip()
        quantidade = self.entry_quantidade.get().strip() or "0"

        if not Metodos.campos_preenchidos(id, nome, tipo, preco):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO produtos (id, nome, tipoProduto, preco, quantidade)
                VALUES (?, ?, ?, ?, ?)
            """, (id, nome, tipo, preco, quantidade))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Produto cadastrado com sucesso!")
            Metodos.limpar_campos(self.entry_id, self.entry_nome, self.entry_tipo,
                                   self.entry_preco, self.entry_quantidade)
        except sqlite3.IntegrityError:
            Metodos.msg_erro("Erro", "ID já cadastrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro ao salvar: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaProduto()

# =================== CONSULTA PRODUTO ===================
class ConsultarProduto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultar Produto")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="CONSULTAR QUANTIDADE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite o ID do Produto:").pack()
        self.entry_id = tk.Entry(self, width=40)
        self.entry_id.pack(pady=5)

        self.label_resultado = tk.Label(self, text="", font=("Arial", 12))
        self.label_resultado.pack(pady=10)

        tk.Button(self, text="Consultar", width=15, command=self.consultar).pack(pady=5)
        tk.Button(self, text="Voltar", width=15, command=self.voltar).pack(pady=5)

        self.mainloop()

    def consultar(self):
        id_prod = self.entry_id.get().strip()
        if not id_prod:
            Metodos.msg_aviso("Atenção", "Digite o ID do produto!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (id_prod,))
            resultado = cursor.fetchone()
            if resultado:
                self.label_resultado.config(text=f"Produto: {resultado[0]}\nQuantidade disponível: {resultado[1]}")
            else:
                self.label_resultado.config(text="Produto não encontrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaProduto()

## =================== MODIFICAR PRODUTO ===================
class ModificarProduto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modificar Produto")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="MODIFICAR PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite o ID do Produto:").pack()
        self.entry_id = tk.Entry(self, width=40)
        self.entry_id.pack(pady=5)

        self.frame_edicao = tk.Frame(self)
        self.frame_edicao.pack(pady=10)

        tk.Button(self, text="Buscar Produto", width=20, command=self.buscar_produto).pack(pady=5)
        tk.Button(self, text="Voltar", width=20, command=self.voltar).pack(pady=5)

        self.mainloop()

    def buscar_produto(self):
        """Busca produto pelo ID e exibe os campos de edição"""
        id_prod = self.entry_id.get().strip()
        if not id_prod:
            Metodos.msg_aviso("Atenção", "Digite o ID do produto!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, tipoProduto, preco, quantidade FROM produtos WHERE id = ?", (id_prod,))
            produto = cursor.fetchone()

            # Limpa o frame de edição antes de criar novos campos
            for widget in self.frame_edicao.winfo_children():
                widget.destroy()

            if produto:
                # Cria campos com valores atuais
                self.entry_nome = Metodos.criar_entry(self.frame_edicao, "Nome:", produto[0])
                self.entry_tipo = Metodos.criar_entry(self.frame_edicao, "Tipo do Produto:", produto[1])
                self.entry_preco = Metodos.criar_entry(self.frame_edicao, "Preço:", produto[2])
                self.entry_quantidade = Metodos.criar_entry(self.frame_edicao, "Quantidade:", produto[3])

                # Botões dentro do frame
                tk.Button(self.frame_edicao, text="Salvar Alterações", width=20, command=self.salvar_alteracoes).pack(pady=5)
                tk.Button(self.frame_edicao, text="Excluir Produto", width=20, fg="red", command=self.excluir_produto).pack(pady=5)
            else:
                Metodos.msg_info("Info", "Produto não encontrado!")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def salvar_alteracoes(self):
        """Atualiza os dados do produto"""
        id_prod = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        tipo = self.entry_tipo.get().strip()
        preco = self.entry_preco.get().strip()
        quantidade = self.entry_quantidade.get().strip() or "0"

        if not Metodos.campos_preenchidos(nome, tipo, preco):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE produtos
                SET nome = ?, tipoProduto = ?, preco = ?, quantidade = ?
                WHERE id = ?
            """, (nome, tipo, preco, quantidade, id_prod))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Produto atualizado com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def excluir_produto(self):
        """Exclui o produto do banco de dados"""
        id_prod = self.entry_id.get().strip()
        if not id_prod:
            Metodos.msg_aviso("Atenção", "Digite o ID do produto!")
            return

        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente excluir este produto?")
        if not confirmar:
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM produtos WHERE id = ?", (id_prod,))
            conexao.commit()

            Metodos.msg_info("Sucesso", "Produto excluído com sucesso!")
            self.entry_id.delete(0, tk.END)
            self.voltar()
            for w in self.frame_edicao.winfo_children():
                w.destroy()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro ao excluir: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaProduto()


if __name__ == "__main__":
    CadastroProduto()
