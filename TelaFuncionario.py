import tkinter as tk
from tkinter import messagebox
import sqlite3
from Metodos import Metodos
from TelaPrincipal import TelaPrincipal

class TelaFuncionario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA FUNCIONÁRIO")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Funcionário", width=30, command=self.tela_cadastro_funcionario).pack(pady=5)
        tk.Button(self, text="Consultar Funcionário", width=30, command=self.consultar_funcionario).pack(pady=5)
        tk.Button(self, text="Modificar Funcionário", width=30, command=self.tela_modificar_funcionario).pack(pady=5)
        tk.Button(self, text="Voltar", width=30, command=self.voltar).pack(pady=25)

        self.mainloop()

    def tela_cadastro_funcionario(self):
        Metodos.limpar_tela(self)

        tk.Label(self, text="TELA CADASTRO FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Nome do Funcionário:").pack()
        self.entry_nome = tk.Entry(self, width=40)
        self.entry_nome.pack(pady=5)

        tk.Label(self, text="CPF:").pack()
        self.entry_cpf = tk.Entry(self, width=40)
        self.entry_cpf.pack(pady=5)
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))

        tk.Label(self, text="Login:").pack()
        self.entry_login = tk.Entry(self, width=40)
        self.entry_login.pack(pady=5)

        tk.Label(self, text="Senha:").pack()
        self.entry_senha = tk.Entry(self, width=40, show="*")
        self.entry_senha.pack(pady=5)

        tk.Button(self, text="Salvar", width=15, command=self.salvar).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_funcionario).pack()

    def salvar(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not Metodos.campos_preenchidos(nome, cpf, login, senha):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO funcionarios (cpf, nome, login, senha)
                VALUES (?, ?, ?, ?)
            """, (cpf, nome, login, senha))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Funcionário cadastrado com sucesso!")
            Metodos.limpar_campos(self.entry_nome, self.entry_cpf, self.entry_login, self.entry_senha)
        except sqlite3.IntegrityError:
            Metodos.msg_erro("Erro", "CPF ou login já cadastrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro ao salvar: {erro}")
        finally:
            Metodos.fechar(conexao)

    def limpar_campos(self):
        Metodos.limpar_campos(self.entry_nome, self.entry_cpf, self.entry_login, self.entry_senha)

    def consultar_funcionario(self):
        Metodos.limpar_tela(self)
        tk.Label(self, text="CONSULTAR FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite CPF do Funcionário:").pack()
        self.entry_consulta = tk.Entry(self, width=40)
        self.entry_consulta.pack(pady=5)
        self.entry_consulta.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_consulta))

        tk.Button(self, text="Consultar", width=15, command=self.exibir_funcionario).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_funcionario).pack(pady=10)

        self.frame_resultado = tk.Frame(self)
        self.frame_resultado.pack(pady=10)

    def exibir_funcionario(self):
        for widget in self.frame_resultado.winfo_children():
            widget.destroy()

        cpf = self.entry_consulta.get().strip()
        if not cpf:
            tk.Label(self.frame_resultado, text="Digite o CPF!", fg="red").pack()
            return

        conexao = Metodos.conectar()
        if not conexao:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, login, senha FROM funcionarios WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                nome, login, senha = resultado
                tk.Label(self.frame_resultado, text=f"Nome: {nome}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(self.frame_resultado, text=f"Login: {login}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(self.frame_resultado, text=f"Senha: {senha}", font=("Arial", 12)).pack(anchor="w")
            else:
                tk.Label(self.frame_resultado, text="Funcionário não encontrado!", fg="red").pack()
        except sqlite3.Error as erro:
            tk.Label(self.frame_resultado, text=f"Ocorreu um erro: {erro}", fg="red").pack()
        finally:
            Metodos.fechar(conexao)

    def tela_modificar_funcionario(self):
        Metodos.limpar_tela(self)
        tk.Label(self, text="MODIFICAR FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite CPF do Funcionário:").pack()
        self.entry_mod_cpf = tk.Entry(self, width=40)
        self.entry_mod_cpf.pack(pady=5)
        self.entry_mod_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_mod_cpf))

        tk.Button(self, text="Buscar Funcionário", width=15, command=self.carregar_funcionario).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_funcionario).pack()

    def carregar_funcionario(self):
        cpf = self.entry_mod_cpf.get().strip()
        if not cpf:
            Metodos.msg_aviso("Atenção", "Digite o CPF!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, login, senha FROM funcionarios WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                nome, login, senha = resultado
                Metodos.limpar_tela(self)

                tk.Label(self, text="MODIFICAR FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

                tk.Label(self, text="Nome:").pack()
                self.entry_nome_mod = tk.Entry(self, width=40)
                self.entry_nome_mod.pack(pady=5)
                self.entry_nome_mod.insert(0, nome)

                tk.Label(self, text="Login:").pack()
                self.entry_login_mod = tk.Entry(self, width=40)
                self.entry_login_mod.pack(pady=5)
                self.entry_login_mod.insert(0, login)

                tk.Label(self, text="Senha:").pack()
                self.entry_senha_mod = tk.Entry(self, width=40)
                self.entry_senha_mod.pack(pady=5)
                self.entry_senha_mod.insert(0, senha)

                tk.Button(self, text="Salvar Alterações", width=15,
                          command=lambda: self.salvar_modificacoes(cpf)).pack(pady=15)
                tk.Button(self, text="Voltar", width=15, command=self.voltar_funcionario).pack()
            else:
                Metodos.msg_info("Não encontrado", "Funcionário não encontrado!")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def salvar_modificacoes(self, cpf):
        nome = self.entry_nome_mod.get().strip()
        login = self.entry_login_mod.get().strip()
        senha = self.entry_senha_mod.get().strip()

        if not Metodos.campos_preenchidos(nome, login, senha):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("UPDATE funcionarios SET nome = ?, login = ?, senha = ? WHERE cpf = ?",
                           (nome, login, senha, cpf))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Dados do funcionário atualizados com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar_funcionario(self):
        self.destroy()
        TelaFuncionario()

    def voltar(self):
        self.destroy()
        TelaPrincipal()

    def limpar_tela(self):
        Metodos.limpar_tela(self)
