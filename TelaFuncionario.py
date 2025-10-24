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
        tk.Button(self, text="Consultar Funcionário", width=30, command=self.consultar_funcionario).pack(pady=5)
        tk.Button(self, text="Modificar Funcionário", width=30, command=self.tela_modificar_funcionario).pack(pady=5)
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
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not nome or not cpf or not login or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO funcionarios (cpf, nome, login, senha)
                VALUES (?, ?, ?, ?)
            """, (cpf, nome, login, senha))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            self.limpar_campos()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {erro}")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

    def consultar_funcionario(self):
        self.limpar_tela()
        tk.Label(self, text="CONSULTAR FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite CPF do Funcionário:").pack()
        self.entry_consulta = tk.Entry(self, width=40)
        self.entry_consulta.pack(pady=5)

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

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, login, senha FROM funcionarios WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()
            conexao.close()

            if resultado:
                nome, login, senha = resultado
                tk.Label(self.frame_resultado, text=f"Nome: {nome}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(self.frame_resultado, text=f"Login: {login}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(self.frame_resultado, text=f"Senha: {senha}", font=("Arial", 12)).pack(anchor="w")
            else:
                tk.Label(self.frame_resultado, text="Funcionário não encontrado!", fg="red").pack()

        except sqlite3.Error as erro:
            tk.Label(self.frame_resultado, text=f"Ocorreu um erro: {erro}", fg="red").pack()


    def tela_modificar_funcionario(self):
        self.limpar_tela()
        tk.Label(self, text="MODIFICAR FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite CPF do Funcionário:").pack()
        self.entry_mod_cpf = tk.Entry(self, width=40)
        self.entry_mod_cpf.pack(pady=5)

        tk.Button(self, text="Buscar Funcionário", width=15, command=self.carregar_funcionario).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_funcionario).pack()

    def carregar_funcionario(self):
        cpf = self.entry_mod_cpf.get().strip()
        if not cpf:
            messagebox.showwarning("Atenção", "Digite o CPF!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, login, senha FROM funcionarios WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()
            conexao.close()

            if resultado:
                nome, login, senha = resultado
                self.limpar_tela()

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
                messagebox.showinfo("Não encontrado", "Funcionário não encontrado!")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

    def salvar_modificacoes(self, cpf):
        nome = self.entry_nome_mod.get().strip()
        login = self.entry_login_mod.get().strip()
        senha = self.entry_senha_mod.get().strip()

        if not nome or not login or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("UPDATE funcionarios SET nome = ?, login = ?, senha = ? WHERE cpf = ?",
                           (nome, login, senha, cpf))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Dados do funcionário atualizados com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")


    def voltar_funcionario(self):
        self.destroy()
        TelaFuncionario()  # Reabre a tela de funcionário

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal  # import dentro da função para evitar loop
        TelaPrincipal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()


