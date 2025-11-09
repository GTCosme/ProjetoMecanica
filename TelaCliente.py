import customtkinter as ctk
from PIL import Image
import sqlite3
from Metodos import Metodos

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# =================== TELA PRINCIPAL CLIENTE ===================
class TelaCliente(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mecânica Masters - Clientes")
        self.geometry("1000x600")
        self.resizable(False, False)

        # =================== NAVBAR ===================
        navbar = ctk.CTkFrame(self, height=60, fg_color="#F8F9FA")
        navbar.pack(fill="x", side="top")

        logo_nav = ctk.CTkImage(
            light_image=Image.open("img/logo.png"),
            dark_image=Image.open("img/logo.png"),
            size=(40, 40)
        )
        logo_label = ctk.CTkLabel(navbar, image=logo_nav, text="")
        logo_label.pack(side="left", padx=20)

        botoes_menu = [
            ("Tela inicial", self.voltar_tela_inicial),
            ("Produtos", self.abrir_tela_produto),
            ("Serviços", self.abrir_tela_servico),
            ("Funcionários", self.abrir_tela_funcionario),
            ("Clientes", lambda: None)
        ]

        for texto, comando in botoes_menu:
            botao = ctk.CTkButton(
                navbar,
                text=texto,
                command=comando,
                fg_color="transparent",
                hover_color="#E1E1E1",
                text_color="#222",
                font=("Arial", 13, "bold"),
                corner_radius=8,
                width=100,
                height=35
            )
            botao.pack(side="left", padx=4)

        # =================== CONTEÚDO ===================
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        titulo = ctk.CTkLabel(
            frame,
            text="Gerenciamento de Clientes",
            font=("Arial Black", 28, "bold"),
            text_color="#222"
        )
        titulo.pack(pady=(80, 30))
        # =================== BOTÕES ===================
        botoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        botoes_frame.pack(pady=40)

        # Botão branco (Cadastrar)
        btn_cadastrar = ctk.CTkButton(
            botoes_frame,
            text="Cadastrar Cliente",
            width=200,
            height=45,
            fg_color="black",
            text_color="white",
            hover_color="#333",
            command=self.abrir_cadastro
        )
        btn_cadastrar.pack(side="left", padx=15)

        # Botão preto (Consultar)
        btn_consultar = ctk.CTkButton(
            botoes_frame,
            text="Consultar Cliente",
            width=200,
            height=45,
            fg_color="white",
            text_color="black",
            hover_color="#E1E1E1",
            command=self.abrir_consultar
        )
        btn_consultar.pack(side="left", padx=15)

        # Botão preto (Modificar)
        btn_modificar = ctk.CTkButton(
            botoes_frame,
            text="Modificar Cliente",
            width=200,
            height=45,
            fg_color="black",
            text_color="white",
            hover_color="#333",
            command=self.abrir_modificar
        )
        btn_modificar.pack(side="left", padx=15)

        self.mainloop()

    # =================== NAVEGAÇÃO ===================
    def abrir_cadastro(self):
        self.destroy()
        CadastroCliente()

    def abrir_consultar(self):
        self.destroy()
        ConsultarCliente()

    def abrir_modificar(self):
        self.destroy()
        ModificarCliente()

    def voltar_tela_inicial(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()

    def abrir_tela_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto
        TelaProduto()

    def abrir_tela_servico(self):
        self.destroy()
        from TelaServico import TelaServico
        TelaServico()

    def abrir_tela_funcionario(self):
        self.destroy()
        from TelaFuncionario import TelaFuncionario
        TelaFuncionario()


# =================== CADASTRO CLIENTE ===================
class CadastroCliente(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cadastrar Cliente")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Cadastrar Cliente", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_nome = Metodos.criar_entry(frame, "Nome do Cliente:")
        self.entry_cpf = Metodos.criar_entry(frame, "CPF:")
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))
        self.entry_telefone = Metodos.criar_entry(frame, "Telefone:")
        self.entry_telefone.bind("<KeyRelease>", lambda e: Metodos.formatar_telefone(self.entry_telefone))
        self.entry_email = Metodos.criar_entry(frame, "Email:")

        ctk.CTkButton(frame, text="Salvar", width=200, height=40, command=self.salvar).pack(pady=20)
        ctk.CTkButton(frame, text="Voltar para Clientes", width=200, height=40, fg_color="#6c757d",
                      command=self.voltar).pack()

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
            ("Funcionários", self.abrir_tela_funcionario),
            ("Clientes", self.voltar)
        ]

        for texto, cmd in botoes:
            ctk.CTkButton(navbar, text=texto, command=cmd,
                          fg_color="transparent", hover_color="#E1E1E1",
                          text_color="#222", font=("Arial", 13, "bold"),
                          width=100, height=35).pack(side="left", padx=4)

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
            cursor.execute("INSERT INTO clientes (cpf, nome, email, telefone) VALUES (?, ?, ?, ?)",
                           (cpf, nome, email, telefone))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Cliente cadastrado com sucesso!")
            Metodos.limpar_campos(self.entry_cpf, self.entry_nome, self.entry_email, self.entry_telefone)
        except sqlite3.IntegrityError:
            Metodos.msg_erro("Erro", "CPF já cadastrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaCliente()

    def voltar_tela_inicial(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()

    def abrir_tela_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto
        TelaProduto()

    def abrir_tela_servico(self):
        self.destroy()
        from TelaServico import TelaServico
        TelaServico()

    def abrir_tela_funcionario(self):
        self.destroy()
        from TelaFuncionario import TelaFuncionario
        TelaFuncionario()


# =================== CONSULTAR CLIENTE ===================
class ConsultarCliente(CadastroCliente):
    def __init__(self):
        super().__init__()
        self.title("Consultar Cliente")
        Metodos.limpar_tela(self)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Consultar Cliente", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_cpf = Metodos.criar_entry(frame, "Digite o CPF do Cliente:")
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))

        ctk.CTkButton(frame, text="Consultar", width=200, height=40, command=self.consultar).pack(pady=20)

        self.frame_resultado = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_resultado.pack(pady=10)

        ctk.CTkButton(frame, text="Voltar para Clientes", width=200, height=40, fg_color="#6c757d",
                      command=self.voltar).pack()

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
            cursor.execute("SELECT nome, telefone, email FROM clientes WHERE cpf = ?", (cpf,))
            cliente = cursor.fetchone()
            if cliente:
                ctk.CTkLabel(self.frame_resultado, text=f"Nome: {cliente[0]}", font=("Arial", 14)).pack(anchor="w")
                ctk.CTkLabel(self.frame_resultado, text=f"Telefone: {cliente[1]}", font=("Arial", 14)).pack(anchor="w")
                ctk.CTkLabel(self.frame_resultado, text=f"Email: {cliente[2]}", font=("Arial", 14)).pack(anchor="w")
            else:
                ctk.CTkLabel(self.frame_resultado, text="Cliente não encontrado!", text_color="red").pack()
        except sqlite3.Error as erro:
            ctk.CTkLabel(self.frame_resultado, text=f"Erro: {erro}", text_color="red").pack()
        finally:
            Metodos.fechar(conexao)


# =================== MODIFICAR CLIENTE ===================
class ModificarCliente(CadastroCliente):
    def __init__(self):
        super().__init__()
        self.title("Modificar Cliente")
        Metodos.limpar_tela(self)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Modificar Cliente", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_cpf = Metodos.criar_entry(frame, "Digite o CPF do Cliente:")
        self.entry_cpf.bind("<KeyRelease>", lambda e: Metodos.formatar_cpf(self.entry_cpf))

        ctk.CTkButton(frame, text="Buscar Cliente", width=200, height=40, command=self.buscar).pack(pady=10)

        self.frame_edicao = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_edicao.pack(pady=10)

        ctk.CTkButton(frame, text="Voltar para Clientes", width=200, height=40, fg_color="#6c757d",
                      command=self.voltar).pack()

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
            cursor.execute("SELECT nome, telefone, email FROM clientes WHERE cpf = ?", (cpf,))
            cliente = cursor.fetchone()

            if cliente:
                self.entry_nome = Metodos.criar_entry(self.frame_edicao, "Nome:", cliente[0])
                self.entry_telefone = Metodos.criar_entry(self.frame_edicao, "Telefone:", cliente[1])
                self.entry_telefone.bind("<KeyRelease>", lambda e: Metodos.formatar_telefone(self.entry_telefone))
                self.entry_email = Metodos.criar_entry(self.frame_edicao, "Email:", cliente[2])

                ctk.CTkButton(self.frame_edicao, text="Salvar Alterações", width=200, height=40,
                              command=lambda: self.salvar(cpf)).pack(pady=15)
            else:
                Metodos.msg_info("Aviso", "Cliente não encontrado!")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def salvar(self, cpf):
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
            cursor.execute("UPDATE clientes SET nome=?, telefone=?, email=? WHERE cpf=?",
                           (nome, telefone, email, cpf))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Cliente atualizado com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)


if __name__ == "__main__":
    TelaCliente()
