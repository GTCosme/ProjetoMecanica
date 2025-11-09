import os

import customtkinter as ctk
from PIL import Image
import sqlite3
from Metodos import Metodos

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# =================== TELA PRINCIPAL FUNCIONÁRIO ===================
class TelaFuncionario(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mecânica Masters - Funcionários")
        self.geometry("1000x600")
        self.resizable(False, False)

        caminho_icon = os.path.join(os.path.dirname(__file__), "img/logo.ico")
        self.iconbitmap(caminho_icon)

        # =================== NAVBAR ===================
        navbar = ctk.CTkFrame(self, height=60, fg_color="#F8F9FA")
        navbar.pack(fill="x", side="top")

        logo_nav = ctk.CTkImage(light_image=Image.open("img/logo.png"), size=(40, 40))
        ctk.CTkLabel(navbar, image=logo_nav, text="").pack(side="left", padx=20)

        botoes_menu = [
            ("Tela inicial", self.voltar_tela_inicial),
            ("Produtos", self.abrir_tela_produto),
            ("Serviços", self.abrir_tela_servico),
            ("Funcionários", lambda: None),
            ("Clientes", self.abrir_tela_cliente)
        ]

        for texto, comando in botoes_menu:
            ctk.CTkButton(navbar, text=texto, command=comando,
                          fg_color="transparent", hover_color="#E1E1E1",
                          text_color="#222", font=("Arial", 13, "bold"),
                          width=100, height=35).pack(side="left", padx=4)

        # =================== CONTEÚDO ===================
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Gerenciamento de Funcionários",
                     font=("Arial Black", 28, "bold"),
                     text_color="#222").pack(pady=(80, 30))

        botoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        botoes_frame.pack(pady=40)

        ctk.CTkButton(botoes_frame, text="Cadastrar Funcionário",
                      width=200, height=45,
                      fg_color="black", text_color="white",
                      hover_color="#333",
                      command=self.abrir_cadastro).pack(side="left", padx=15)

        ctk.CTkButton(botoes_frame, text="Consultar Funcionário",
                      width=200, height=45,
                      fg_color="white", text_color="black",
                      hover_color="#E1E1E1",
                      command=self.abrir_consultar).pack(side="left", padx=15)

        ctk.CTkButton(botoes_frame, text="Modificar Funcionário",
                      width=200, height=45,
                      fg_color="black", text_color="white",
                      hover_color="#333",
                      command=self.abrir_modificar).pack(side="left", padx=15)

        self.mainloop()

    # =================== NAVEGAÇÃO ===================
    def abrir_cadastro(self):
        self.destroy()
        CadastroFuncionario()

    def abrir_consultar(self):
        self.destroy()
        ConsultarFuncionario()

    def abrir_modificar(self):
        self.destroy()
        ModificarFuncionario()

    def voltar_tela_inicial(self):
        from TelaPrincipal import TelaPrincipal
        self.destroy()
        TelaPrincipal().mainloop()

    def abrir_tela_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto
        TelaProduto()

    def abrir_tela_servico(self):
        self.destroy()
        from TelaServico import TelaServico
        TelaServico()

    def abrir_tela_cliente(self):
        self.destroy()
        from TelaCliente import TelaCliente
        TelaCliente()


# =================== CADASTRO FUNCIONÁRIO ===================
class CadastroFuncionario(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cadastrar Funcionário")
        self.geometry("1000x600")
        self.resizable(False, False)

        caminho_icon = os.path.join(os.path.dirname(__file__), "img/logo.ico")
        self.iconbitmap(caminho_icon)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Cadastrar Funcionário", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_nome = Metodos.criar_entry(frame, "Nome do Funcionário:")
        self.entry_cpf = Metodos.criar_entry(frame, "CPF:")
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))
        self.entry_login = Metodos.criar_entry(frame, "Login:")
        self.entry_senha = Metodos.criar_entry(frame, "Senha:")

        ctk.CTkButton(frame, text="Salvar", width=200, height=40, command=self.salvar).pack(pady=20)
        ctk.CTkButton(frame, text="Voltar para Funcionários", width=200, height=40,
                      fg_color="#6c757d", command=self.voltar).pack()

        self.mainloop()

    def criar_navbar(self):
        navbar = ctk.CTkFrame(self, height=60, fg_color="#F8F9FA")
        navbar.pack(fill="x", side="top")

        logo_nav = ctk.CTkImage(light_image=Image.open("img/logo.png"), size=(40, 40))
        ctk.CTkLabel(navbar, image=logo_nav, text="").pack(side="left", padx=20)

        botoes = [
            ("Tela inicial", self.voltar_tela_inicial),
            ("Produtos", self.abrir_tela_produto),
            ("Serviços", self.abrir_tela_servico),
            ("Funcionários", self.voltar),
            ("Clientes", self.abrir_tela_cliente)
        ]

        for texto, cmd in botoes:
            ctk.CTkButton(navbar, text=texto, command=cmd,
                          fg_color="transparent", hover_color="#E1E1E1",
                          text_color="#222", font=("Arial", 13, "bold"),
                          width=100, height=35).pack(side="left", padx=4)

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
            cursor.execute("INSERT INTO funcionarios (cpf, nome, login, senha) VALUES (?, ?, ?, ?)",
                           (cpf, nome, login, senha))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Funcionário cadastrado com sucesso!")
            Metodos.limpar_campos(self.entry_nome, self.entry_cpf, self.entry_login, self.entry_senha)
        except sqlite3.IntegrityError:
            Metodos.msg_erro("Erro", "CPF ou login já cadastrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaFuncionario()

    # Navegação comum
    def voltar_tela_inicial(self):
        from TelaPrincipal import TelaPrincipal
        self.destroy()
        TelaPrincipal().mainloop()
    def abrir_tela_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto
        TelaProduto()

    def abrir_tela_servico(self):
        self.destroy()
        from TelaServico import TelaServico
        TelaServico()

    def abrir_tela_cliente(self):
        self.destroy()
        from TelaCliente import TelaCliente
        TelaCliente()


# =================== CONSULTAR FUNCIONÁRIO ===================
class ConsultarFuncionario(CadastroFuncionario):
    def __init__(self):
        super().__init__()
        self.title("Consultar Funcionário")
        Metodos.limpar_tela(self)

        caminho_icon = os.path.join(os.path.dirname(__file__), "img/logo.ico")
        self.iconbitmap(caminho_icon)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Consultar Funcionário", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_cpf = Metodos.criar_entry(frame, "Digite o CPF do Funcionário:")
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))

        ctk.CTkButton(frame, text="Consultar", width=200, height=40, command=self.consultar).pack(pady=20)

        self.frame_resultado = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_resultado.pack(pady=10)

        ctk.CTkButton(frame, text="Voltar para Funcionários", width=200, height=40,
                      fg_color="#6c757d", command=self.voltar).pack()

    def consultar(self):
        for w in self.frame_resultado.winfo_children():
            w.destroy()

        cpf = self.entry_cpf.get().strip()
        if not cpf:
            ctk.CTkLabel(self.frame_resultado, text="Digite o CPF!", text_color="red").pack()
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, login, senha FROM funcionarios WHERE cpf = ?", (cpf,))
            func = cursor.fetchone()
            if func:
                ctk.CTkLabel(self.frame_resultado, text=f"Nome: {func[0]}", font=("Arial", 14)).pack(anchor="w")
                ctk.CTkLabel(self.frame_resultado, text=f"Login: {func[1]}", font=("Arial", 14)).pack(anchor="w")
                ctk.CTkLabel(self.frame_resultado, text=f"Senha: {func[2]}", font=("Arial", 14)).pack(anchor="w")
            else:
                ctk.CTkLabel(self.frame_resultado, text="Funcionário não encontrado!", text_color="red").pack()
        except sqlite3.Error as erro:
            ctk.CTkLabel(self.frame_resultado, text=f"Erro: {erro}", text_color="red").pack()
        finally:
            Metodos.fechar(conexao)


# =================== MODIFICAR FUNCIONÁRIO ===================
class ModificarFuncionario(CadastroFuncionario):
    def __init__(self):
        super().__init__()
        self.title("Modificar Funcionário")
        Metodos.limpar_tela(self)

        caminho_icon = os.path.join(os.path.dirname(__file__), "img/logo.ico")
        self.iconbitmap(caminho_icon)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Modificar Funcionário", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_cpf = Metodos.criar_entry(frame, "Digite o CPF do Funcionário:")
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))

        ctk.CTkButton(frame, text="Buscar Funcionário", width=200, height=40, command=self.buscar).pack(pady=10)

        self.frame_edicao = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_edicao.pack(pady=10)

        ctk.CTkButton(frame, text="Voltar para Funcionários", width=200, height=40,
                      fg_color="#6c757d", command=self.voltar).pack()

    def buscar(self):
        for w in self.frame_edicao.winfo_children():
            w.destroy()

        cpf = self.entry_cpf.get().strip()
        if not cpf:
            Metodos.msg_aviso("Atenção", "Digite o CPF!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, login, senha FROM funcionarios WHERE cpf = ?", (cpf,))
            func = cursor.fetchone()
            if func:
                self.entry_nome = Metodos.criar_entry(self.frame_edicao, "Nome:", func[0])
                self.entry_login = Metodos.criar_entry(self.frame_edicao, "Login:", func[1])
                self.entry_senha = Metodos.criar_entry(self.frame_edicao, "Senha:", func[2])

                ctk.CTkButton(self.frame_edicao, text="Salvar Alterações", width=200, height=40,
                              command=lambda: self.salvar(cpf)).pack(pady=15)
            else:
                Metodos.msg_info("Aviso", "Funcionário não encontrado!")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def salvar(self, cpf):
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not Metodos.campos_preenchidos(nome, login, senha):
            Metodos.msg_aviso("Atenção", "Preencha todos os campos!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("UPDATE funcionarios SET nome=?, login=?, senha=? WHERE cpf=?",
                           (nome, login, senha, cpf))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Funcionário atualizado com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)


if __name__ == "__main__":
    TelaFuncionario()
