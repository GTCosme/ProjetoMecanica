import customtkinter as ctk
from PIL import Image, ImageEnhance
from Metodos import Metodos

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TelaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mecânica Masters - Tela Principal")
        self.geometry("1000x600")
        self.resizable(False, False)

        # ======================
        # IMAGEM DE FUNDO (LOGO CENTRAL TRANSPARENTE)
        # ======================
        logo_original = Image.open("img/logo.png").convert("RGBA")

        alpha = 0.15  # transparência
        logo_transparente = logo_original.copy()
        logo_transparente.putalpha(int(255 * alpha))
        logo_transparente.save("img/logo_fundo_temp.png")

        bg_image = ctk.CTkImage(
            light_image=Image.open("img/logo_fundo_temp.png"),
            dark_image=Image.open("img/logo_fundo_temp.png"),
            size=(500, 500)
        )
        bg_label = ctk.CTkLabel(self, image=bg_image, text="")
        bg_label.place(relx=0.5, rely=0.5, anchor="center")
        bg_label.lower()

        # ======================
        # BARRA DE NAVEGAÇÃO
        # ======================
        navbar = ctk.CTkFrame(self, height=60, fg_color="#F8F9FA")
        navbar.pack(fill="x", side="top")

        # Logo pequeno
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
            ("Clientes", self.abrir_tela_cliente)
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

        # ======== BOTÃO DE USUÁRIO ========
        user_icon = ctk.CTkImage(light_image=Image.open("img/user.png"), size=(25, 25))

        user_btn = ctk.CTkButton(
            navbar,
            image=user_icon,
            text="",  # sem texto
            width=40,
            height=40,
            fg_color="white",
            hover_color="#E1E1E1",
            corner_radius=20,
            command=self.abrir_perfil
        )
        user_btn.pack(side="right", padx=20)

        # ======================
        # CONTEÚDO CENTRAL
        # ======================
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        titulo = ctk.CTkLabel(
            main_frame,
            text="Mecânica Masters",
            font=("Arial Black", 38, "bold"),
            text_color="#222"
        )
        titulo.pack(pady=(150, 10))

        subtitulo = ctk.CTkLabel(
            main_frame,
            text="Bem-vindo(a)! Escolha uma opção acima para começar.",
            font=("Arial", 18),
            text_color="#444"
        )
        subtitulo.pack()

    # ======================
    # FUNÇÕES DE NAVEGAÇÃO
    # ======================
    def voltar_tela_inicial(self):
        pass

    def abrir_tela_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto
        app = TelaProduto()
        app.mainloop()

    def abrir_tela_servico(self):
        self.destroy()
        from TelaServico import TelaServico
        TelaServico()

    def abrir_tela_funcionario(self):
        self.destroy()
        from TelaFuncionario import TelaFuncionario
        TelaFuncionario()

    def abrir_tela_cliente(self):
        self.destroy()
        from TelaCliente import TelaCliente
        TelaCliente()

    def abrir_perfil(self):
        self.destroy()
        from TelaLogin import TelaLogin
        TelaLogin()


if __name__ == "__main__":
    TelaPrincipal().mainloop()
