import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from Metodos import Metodos


# =================== TELA PRINCIPAL SERVIÇO ===================
class TelaServico(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA SERVIÇO")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA SERVIÇO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Serviço", width=25, command=self.abrir_cadastro).pack(pady=5)
        tk.Button(self, text="Consultar Serviço", width=25, command=self.abrir_consultar).pack(pady=5)
        tk.Button(self, text="Modificar Serviço", width=25, command=self.abrir_modificar).pack(pady=5)
        tk.Button(self, text="Voltar", width=25, command=self.voltar).pack(pady=20)

        self.mainloop()

    def abrir_cadastro(self):
        self.destroy()
        CadastroServico()

    def abrir_consultar(self):
        self.destroy()
        ConsultarServico()

    def abrir_modificar(self):
        self.destroy()
        ModificarServico()

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()


# =================== CADASTRAR SERVIÇO ===================
class CadastroServico(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastrar Serviço")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="CADASTRAR SERVIÇO", font=("Arial", 16, "bold")).pack(pady=20)

        self.entry_id = Metodos.criar_entry(self, "ID:")
        self.entry_servico = Metodos.criar_entry(self, "Serviço:")
        self.entry_preco = Metodos.criar_entry(self, "Preço:")
        self.entry_preco.bind("<FocusOut>", lambda e: Metodos.formatar_moeda(self.entry_preco))

        # Campo de funcionário responsável
        tk.Label(self, text="Funcionário Responsável:").pack()
        self.combo_funcionario = ttk.Combobox(self, width=37, state="readonly")
        self.combo_funcionario.pack(pady=5)
        self.carregar_funcionarios()

        tk.Button(self, text="Salvar", width=15, command=self.salvar).pack(pady=10)
        tk.Button(self, text="Voltar", width=15, command=self.voltar).pack(pady=5)

        self.mainloop()

    def carregar_funcionarios(self):
        conexao = Metodos.conectar()
        if not conexao:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM funcionarios")
            nomes = [row[0] for row in cursor.fetchall()]
            self.combo_funcionario["values"] = nomes
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Erro ao carregar funcionários: {erro}")
        finally:
            Metodos.fechar(conexao)

    def salvar(self):
        id = self.entry_id.get().strip()
        servico = self.entry_servico.get().strip()
        preco = self.entry_preco.get().strip()
        funcionario = self.combo_funcionario.get().strip()

        if not Metodos.campos_preenchidos(id, servico, preco, funcionario):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO servicos (id, servico, preco, funcionarioResponsavel)
                VALUES (?, ?, ?, ?)
            """, (id, servico, preco, funcionario))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Serviço cadastrado com sucesso!")
            Metodos.limpar_campos(self.entry_id, self.entry_servico, self.entry_preco)
            self.combo_funcionario.set("")
        except sqlite3.IntegrityError:
            Metodos.msg_erro("Erro", "ID já cadastrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro ao salvar: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaServico()


# =================== CONSULTAR SERVIÇO ===================
class ConsultarServico(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultar Serviço")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="CONSULTAR SERVIÇO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite o ID do Serviço:").pack()
        self.entry_id = tk.Entry(self, width=40)
        self.entry_id.pack(pady=5)

        self.label_resultado = tk.Label(self, text="", font=("Arial", 12))
        self.label_resultado.pack(pady=10)

        tk.Button(self, text="Consultar", width=15, command=self.consultar).pack(pady=5)
        tk.Button(self, text="Voltar", width=15, command=self.voltar).pack(pady=5)

        self.mainloop()

    def consultar(self):
        id_serv = self.entry_id.get().strip()
        if not id_serv:
            Metodos.msg_aviso("Atenção", "Digite o ID do serviço!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT servico, preco, funcionarioResponsavel FROM servicos WHERE id = ?", (id_serv,))
            resultado = cursor.fetchone()
            if resultado:
                self.label_resultado.config(
                    text=f"Serviço: {resultado[0]}\nPreço: {resultado[1]}\nFuncionário: {resultado[2]}"
                )
            else:
                self.label_resultado.config(text="Serviço não encontrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaServico()


# =================== MODIFICAR SERVIÇO ===================
class ModificarServico(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modificar Serviço")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="MODIFICAR SERVIÇO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite o ID do Serviço:").pack()
        self.entry_id = tk.Entry(self, width=40)
        self.entry_id.pack(pady=5)

        self.frame_edicao = tk.Frame(self)
        self.frame_edicao.pack(pady=10)

        self.botao_buscar = tk.Button(self, text="Buscar Serviço", width=20, command=self.buscar_servico)
        self.botao_buscar.pack(pady=5)
        tk.Button(self, text="Voltar", width=20, command=self.voltar).pack(pady=5)

        self.mainloop()

    def buscar_servico(self):
        id_serv = self.entry_id.get().strip()
        if not id_serv:
            Metodos.msg_aviso("Atenção", "Digite o ID do serviço!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT servico, preco, funcionarioResponsavel FROM servicos WHERE id = ?", (id_serv,))
            servico = cursor.fetchone()

            for w in self.frame_edicao.winfo_children():
                w.destroy()

            if servico:
                self.botao_buscar.destroy()

                self.entry_servico = Metodos.criar_entry(self.frame_edicao, "Serviço:", servico[0])
                self.entry_preco = Metodos.criar_entry(self.frame_edicao, "Preço:", servico[1])

                tk.Label(self.frame_edicao, text="Funcionário Responsável:").pack()
                self.combo_funcionario = ttk.Combobox(self.frame_edicao, width=37, state="readonly")
                self.combo_funcionario.pack(pady=5)
                self.carregar_funcionarios()
                self.combo_funcionario.set(servico[2])

                tk.Button(self.frame_edicao, text="Salvar Alterações", width=20,
                          command=self.salvar_alteracoes).pack(pady=5)
                tk.Button(self.frame_edicao, text="Excluir Serviço", width=20, fg="red",
                          command=self.excluir_servico).pack(pady=5)
            else:
                Metodos.msg_info("Info", "Serviço não encontrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def carregar_funcionarios(self):
        conexao = Metodos.conectar()
        if not conexao:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM funcionarios")
            nomes = [row[0] for row in cursor.fetchall()]
            self.combo_funcionario["values"] = nomes
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Erro ao carregar funcionários: {erro}")
        finally:
            Metodos.fechar(conexao)

    def salvar_alteracoes(self):
        id_serv = self.entry_id.get().strip()
        servico = self.entry_servico.get().strip()
        preco = self.entry_preco.get().strip()
        funcionario = self.combo_funcionario.get().strip()

        if not Metodos.campos_preenchidos(servico, preco, funcionario):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE servicos
                SET servico = ?, preco = ?, funcionarioResponsavel = ?
                WHERE id = ?
            """, (servico, preco, funcionario, id_serv))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Serviço atualizado com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def excluir_servico(self):
        id_serv = self.entry_id.get().strip()
        if not id_serv:
            Metodos.msg_aviso("Atenção", "Digite o ID do serviço!")
            return

        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente excluir este serviço?")
        if not confirmar:
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM servicos WHERE id = ?", (id_serv,))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Serviço excluído com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro ao excluir: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaServico()


if __name__ == "__main__":
    TelaServico()
