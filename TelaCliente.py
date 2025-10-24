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
        tk.Button(self, text="Consultar Cliente", width=30, command=self.consultar_cliente).pack(pady=5)
        tk.Button(self, text="Modificar Cliente", width=30, command=self.tela_modificar_cliente).pack(pady=5)
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
            self.limpar_campos()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {erro}")

    def limpar_campos(self):
        self.entry_cpf.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)


    def consultar_cliente(self):
        self.limpar_tela()
        tk.Label(self, text="CONSULTAR CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite CPF do Cliente:").pack()
        self.entry_consulta = tk.Entry(self, width=40)
        self.entry_consulta.pack(pady=5)

        tk.Button(self, text="Consultar", width=15, command=self.exibir_cliente).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_cliente).pack(pady=10)


        self.frame_resultado = tk.Frame(self)
        self.frame_resultado.pack(pady=10)

    def exibir_cliente(self):

        for widget in self.frame_resultado.winfo_children():
            widget.destroy()

        cpf = self.entry_consulta.get().strip()
        if not cpf:
            tk.Label(self.frame_resultado, text="Digite o CPF!", fg="red").pack()
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, telefone, email FROM clientes WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()
            conexao.close()

            if resultado:
                nome, telefone, email = resultado
                tk.Label(self.frame_resultado, text=f"Nome: {nome}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(self.frame_resultado, text=f"Telefone: {telefone}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(self.frame_resultado, text=f"Email: {email}", font=("Arial", 12)).pack(anchor="w")
            else:
                tk.Label(self.frame_resultado, text="Cliente não encontrado!", fg="red").pack()

        except sqlite3.Error as erro:
            tk.Label(self.frame_resultado, text=f"Ocorreu um erro: {erro}", fg="red").pack()


    def tela_modificar_cliente(self):
        self.limpar_tela()
        tk.Label(self, text="MODIFICAR CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Digite CPF do Cliente:").pack()
        self.entry_mod_cpf = tk.Entry(self, width=40)
        self.entry_mod_cpf.pack(pady=5)

        tk.Button(self, text="Buscar Cliente", width=15, command=self.carregar_cliente).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_cliente).pack()

    def carregar_cliente(self):
        cpf = self.entry_mod_cpf.get().strip()
        if not cpf:
            messagebox.showwarning("Atenção", "Digite o CPF!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, telefone, email FROM clientes WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()
            conexao.close()

            if resultado:
                nome, telefone, email = resultado
                self.limpar_tela()

                tk.Label(self, text="MODIFICAR CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

                tk.Label(self, text="Nome:").pack()
                self.entry_nome_mod = tk.Entry(self, width=40)
                self.entry_nome_mod.pack(pady=5)
                self.entry_nome_mod.insert(0, nome)

                tk.Label(self, text="Telefone:").pack()
                self.entry_telefone_mod = tk.Entry(self, width=40)
                self.entry_telefone_mod.pack(pady=5)
                self.entry_telefone_mod.insert(0, telefone)

                tk.Label(self, text="Email:").pack()
                self.entry_email_mod = tk.Entry(self, width=40)
                self.entry_email_mod.pack(pady=5)
                self.entry_email_mod.insert(0, email)

                tk.Button(self, text="Salvar Alterações", width=15,
                          command=lambda: self.salvar_modificacoes(cpf)).pack(pady=15)
                tk.Button(self, text="Voltar", width=15, command=self.voltar_cliente).pack()
            else:
                messagebox.showinfo("Não encontrado", "Cliente não encontrado!")
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

    def salvar_modificacoes(self, cpf):
        nome = self.entry_nome_mod.get().strip()
        telefone = self.entry_telefone_mod.get().strip()
        email = self.entry_email_mod.get().strip()

        if not nome or not telefone or not email:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conexao = sqlite3.connect("mecanica_master.db")
            cursor = conexao.cursor()
            cursor.execute("UPDATE clientes SET nome = ?, telefone = ?, email = ? WHERE cpf = ?",
                           (nome, telefone, email, cpf))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Dados do cliente atualizados com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

    def voltar_cliente(self):
        self.destroy()
        TelaCliente()  # Reabre a tela de cliente

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal  # Import dentro da função para evitar loop
        TelaPrincipal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()


