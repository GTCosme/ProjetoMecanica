import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from Metodos import Metodos
from PIL import Image


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# =================== TELA PRINCIPAL PRODUTO ===================
class TelaProduto(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mecânica Masters - Produtos")
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
            ("Serviços", self.abrir_tela_servico),
            ("Funcionários", self.abrir_tela_funcionario),
            ("Clientes", self.abrir_tela_cliente),
            ("Produtos", lambda: None)
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
            text="Gerenciamento de Produtos",
            font=("Arial Black", 28, "bold"),
            text_color="#222"
        )
        titulo.pack(pady=(80, 30))

        # =================== BOTÕES ===================
        botoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        botoes_frame.pack(pady=40)

        btn_cadastrar = ctk.CTkButton(
            botoes_frame,
            text="Cadastrar Produto",
            width=200,
            height=45,
            fg_color="white",
            text_color="black",
            hover_color="#E1E1E1",
            command=self.abrir_cadastro
        )
        btn_cadastrar.pack(side="left", padx=15)

        btn_consultar = ctk.CTkButton(
            botoes_frame,
            text="Consultar Produto",
            width=200,
            height=45,
            fg_color="black",
            text_color="white",
            hover_color="#333",
            command=self.abrir_consultar
        )
        btn_consultar.pack(side="left", padx=15)

        btn_modificar = ctk.CTkButton(
            botoes_frame,
            text="Modificar Produto",
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
        CadastroProduto()

    def abrir_consultar(self):
        self.destroy()
        ConsultarProduto()

    def abrir_modificar(self):
        self.destroy()
        ModificarProduto()

    def voltar_tela_inicial(self):
        from TelaPrincipal import TelaPrincipal
        self.destroy()
        TelaPrincipal()

    def abrir_tela_servico(self):
        from TelaServico import TelaServico
        self.destroy()
        TelaServico()

    def abrir_tela_funcionario(self):
        from TelaFuncionario import TelaFuncionario
        self.destroy()
        TelaFuncionario()

    def abrir_tela_cliente(self):
        from TelaCliente import TelaCliente
        self.destroy()
        TelaCliente()

    def voltar_tela_inicial(self):
         from TelaPrincipal import TelaPrincipal
         self.destroy()
         TelaPrincipal().mainloop


# =================== CADASTRAR PRODUTO ===================
class CadastroProduto(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cadastrar Produto")
        self.geometry("1000x600")
        self.resizable(False, False)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Cadastro de Produto", font=("Arial Black", 26, "bold")).pack(pady=20)

        self.entry_id = Metodos.criar_entry(frame, "ID:")
        self.entry_nome = Metodos.criar_entry(frame, "Nome:")
        self.entry_tipo = Metodos.criar_entry(frame, "Tipo:")
        self.entry_preco = Metodos.criar_entry(frame, "Preço:")
        self.entry_preco.bind("<KeyRelease>", lambda e: Metodos.formatar_moeda(self.entry_preco))
        self.entry_quantidade = Metodos.criar_entry(frame, "Quantidade:")

        botoes = ctk.CTkFrame(frame, fg_color="transparent")
        botoes.pack(pady=30)
        ctk.CTkButton(botoes, text="Salvar", width=160, command=self.salvar).pack(pady=5)
        ctk.CTkButton(botoes, text="Voltar", width=160, fg_color="#AAB7B8",
                      hover_color="#909497", command=self.voltar).pack(pady=5)

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
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaProduto()


# =================== CONSULTAR PRODUTO ===================
class ConsultarProduto(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Consultar Produto")
        self.geometry("1000x600")
        self.resizable(False, False)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Consultar Produto", font=("Arial Black", 26, "bold")).pack(pady=20)

        ctk.CTkLabel(frame, text="Digite o ID do produto:", font=("Arial", 14)).pack(pady=5)
        self.entry_id = ctk.CTkEntry(frame, width=300)
        self.entry_id.pack(pady=5)

        self.label_resultado = ctk.CTkLabel(frame, text="", font=("Arial", 14))
        self.label_resultado.pack(pady=15)

        botoes = ctk.CTkFrame(frame, fg_color="transparent")
        botoes.pack(pady=30)
        ctk.CTkButton(botoes, text="Consultar", width=160, command=self.consultar).pack(pady=5)
        ctk.CTkButton(botoes, text="Voltar", width=160, fg_color="#AAB7B8",
                      hover_color="#909497", command=self.voltar).pack(pady=5)

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
                self.label_resultado.configure(
                    text=f"Produto: {resultado[0]}\nQuantidade disponível: {resultado[1]}"
                )
            else:
                self.label_resultado.configure(text="Produto não encontrado.")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaProduto()


# =================== MODIFICAR PRODUTO ===================
class ModificarProduto(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modificar Produto")
        self.geometry("1000x600")
        self.resizable(False, False)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Modificar Produto", font=("Arial Black", 26, "bold")).pack(pady=20)

        ctk.CTkLabel(frame, text="Digite o ID do produto:", font=("Arial", 14)).pack()
        self.entry_id = ctk.CTkEntry(frame, width=300)
        self.entry_id.pack(pady=5)

        ctk.CTkButton(frame, text="Buscar Produto", width=160, command=self.buscar_produto).pack(pady=10)

        self.frame_edicao = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_edicao.pack(pady=10)

        ctk.CTkButton(frame, text="Voltar", width=160, fg_color="#AAB7B8",
                      hover_color="#909497", command=self.voltar).pack(pady=15)

        self.mainloop()

    def buscar_produto(self):
        id_prod = self.entry_id.get().strip()
        if not id_prod:
            Metodos.msg_aviso("Atenção", "Digite o ID!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        for widget in self.frame_edicao.winfo_children():
            widget.destroy()

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, tipoProduto, preco, quantidade FROM produtos WHERE id=?", (id_prod,))
            produto = cursor.fetchone()

            if produto:
                self.entry_nome = Metodos.criar_entry(self.frame_edicao, "Nome:", produto[0])
                self.entry_tipo = Metodos.criar_entry(self.frame_edicao, "Tipo:", produto[1])
                self.entry_preco = Metodos.criar_entry(self.frame_edicao, "Preço:", produto[2])
                self.entry_quantidade = Metodos.criar_entry(self.frame_edicao, "Quantidade:", produto[3])

                ctk.CTkButton(self.frame_edicao, text="Salvar Alterações",
                              width=160, command=lambda: self.salvar_alteracoes(id_prod)).pack(pady=10)
            else:
                Metodos.msg_info("Info", "Produto não encontrado.")
        finally:
            Metodos.fechar(conexao)

    def salvar_alteracoes(self, id_prod):
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
                SET nome=?, tipoProduto=?, preco=?, quantidade=?
                WHERE id=?
            """, (nome, tipo, preco, quantidade, id_prod))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Produto atualizado com sucesso!")
            self.voltar()
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaProduto()


if __name__ == "__main__":
    TelaProduto()
