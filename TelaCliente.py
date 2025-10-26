import sqlite3
import tkinter as tk
from tkinter import messagebox
from Metodos import Metodos
from TelaPrincipal import TelaPrincipal

# =================== TELA PRINCIPAL CLIENTE ===================
class TelaCliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA CLIENTE")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Cliente", width=25, command=self.abrir_cadastro).pack(pady=5)
        tk.Button(self, text="Consultar Cliente", width=25, command=self.abrir_consultar).pack(pady=5)
        tk.Button(self, text="Modificar Cliente", width=25, command=self.abrir_modificar).pack(pady=5)
        tk.Button(self, text="Voltar", width=25, command=self.voltar).pack(pady=20)

        self.mainloop()

    def abrir_cadastro(self):
        self.destroy()
        CadastroCliente()

    def abrir_consultar(self):
        self.destroy()
        ConsultarCliente()

    def abrir_modificar(self):
        self.destroy()
        ModificarCliente()

    def voltar(self):
        self.destroy()
        TelaPrincipal()


# =================== CADASTRO CLIENTE ===================
class CadastroCliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastrar Cliente")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA CADASTRO CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        self.entry_nome = Metodos.criar_entry(self, "Nome do Cliente:")
        self.entry_cpf = Metodos.criar_entry(self, "CPF:")
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))
        self.entry_telefone = Metodos.criar_entry(self, "Telefone:")
        self.entry_telefone.bind("<KeyRelease>", lambda e: Metodos.formatar_telefone(self.entry_telefone))
        self.entry_email = Metodos.criar_entry(self, "Email:")

        tk.Button(self, text="Salvar", width=15, command=self.salvar).pack(pady=10)
        tk.Button(self, text="Voltar", width=15, command=self.voltar).pack(pady=5)

        self.mainloop()

    def salvar(self):
        cpf = self.entry_cpf.get().strip()
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        if not Metodos.campos_preenchidos(cpf, nome, email, telefone):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        if not Metodos.validar_email(email):
            Metodos.msg_aviso("Atenção", "Email inválido!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO clientes (cpf, nome, email, telefone)
                VALUES (?, ?, ?, ?)
            """, (cpf, nome, email, telefone))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Cliente cadastrado com sucesso!")
            Metodos.limpar_campos(self.entry_cpf, self.entry_nome, self.entry_email, self.entry_telefone)
        except sqlite3.IntegrityError:
            Metodos.msg_erro("Erro", "CPF já cadastrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro ao salvar: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaCliente()


# =================== CONSULTAR CLIENTE ===================
class ConsultarCliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultar Cliente")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="CONSULTAR CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        self.entry_cpf = Metodos.criar_entry(self, "Digite o CPF do Cliente:")
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))

        self.frame_resultado = tk.Frame(self)
        self.frame_resultado.pack(pady=10)

        tk.Button(self, text="Consultar", width=15, command=self.consultar).pack(pady=5)
        tk.Button(self, text="Voltar", width=15, command=self.voltar).pack(pady=5)

        self.mainloop()

    def consultar(self):
        for w in self.frame_resultado.winfo_children():
            w.destroy()

        cpf = self.entry_cpf.get().strip()
        if not cpf:
            tk.Label(self.frame_resultado, text="Digite o CPF!", fg="red").pack()
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, telefone, email FROM clientes WHERE cpf = ?", (cpf,))
            cliente = cursor.fetchone()
            if cliente:
                tk.Label(self.frame_resultado, text=f"Nome: {cliente[0]}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(self.frame_resultado, text=f"Telefone: {cliente[1]}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(self.frame_resultado, text=f"Email: {cliente[2]}", font=("Arial", 12)).pack(anchor="w")
            else:
                tk.Label(self.frame_resultado, text="Cliente não encontrado!", fg="red").pack()
        except sqlite3.Error as erro:
            tk.Label(self.frame_resultado, text=f"Ocorreu um erro: {erro}", fg="red").pack()
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaCliente()


# =================== MODIFICAR CLIENTE ===================
class ModificarCliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modificar Cliente")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="MODIFICAR CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        self.entry_cpf_busca = Metodos.criar_entry(self, "Digite o CPF do Cliente:")
        self.entry_cpf_busca.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf_busca))

        self.frame_edicao = tk.Frame(self)
        self.frame_edicao.pack(pady=10)

        # Guardar referência do botão
        self.botao_buscar = tk.Button(self, text="Buscar Cliente", width=20, command=self.buscar_cliente)
        self.botao_buscar.pack(pady=5)

        tk.Button(self, text="Voltar", width=20, command=self.voltar).pack(pady=5)

        self.mainloop()

    def buscar_cliente(self):
        cpf = self.entry_cpf_busca.get().strip()
        if not cpf:
            Metodos.msg_aviso("Atenção", "Digite o CPF!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, telefone, email FROM clientes WHERE cpf = ?", (cpf,))
            cliente = cursor.fetchone()

            # Limpa frame de edição
            for w in self.frame_edicao.winfo_children():
                w.destroy()

            if cliente:
                self.botao_buscar.destroy()
                self.entry_nome = Metodos.criar_entry(self.frame_edicao, "Nome:", cliente[0])
                self.entry_telefone = Metodos.criar_entry(self.frame_edicao, "Telefone:", cliente[1])
                self.entry_telefone.bind("<KeyRelease>", lambda e: Metodos.formatar_telefone(self.entry_telefone))
                self.entry_email = Metodos.criar_entry(self.frame_edicao, "Email:", cliente[2])

                tk.Button(self.frame_edicao, text="Salvar Alterações", width=20,
                          command=lambda: self.salvar_alteracoes(cpf)).pack(pady=5)
                tk.Button(self.frame_edicao, text="Excluir Cliente", width=20, fg="red",
                          command=lambda: self.excluir_cliente(cpf)).pack(pady=5)
            else:
                Metodos.msg_info("Não encontrado", "Cliente não encontrado!")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def salvar_alteracoes(self, cpf):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()

        if not Metodos.campos_preenchidos(nome, telefone, email):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        if not Metodos.validar_email(email):
            Metodos.msg_aviso("Atenção", "Email inválido!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nome = ?, telefone = ?, email = ?
                WHERE cpf = ?
            """, (nome, telefone, email, cpf))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Dados do cliente atualizados com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def excluir_cliente(self, cpf):
        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?")
        if not confirmar:
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Cliente excluído com sucesso!")
            for w in self.frame_edicao.winfo_children():
                self.voltar()
                w.destroy()
            self.entry_cpf_busca.delete(0, tk.END)
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro ao excluir: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaCliente()


if __name__ == "__main__":
    TelaCliente()
