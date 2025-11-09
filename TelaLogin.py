import os

import customtkinter as ctk
import sqlite3
from Metodos import Metodos
from TelaPrincipal import TelaPrincipal


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mecânica Masters - Login")
        self.geometry("1000x600")
        self.resizable(False, False)

        caminho_icon = os.path.join(os.path.dirname(__file__), "img/logo.ico")
        self.iconbitmap(caminho_icon)

        # ======================
        # CONTEÚDO CENTRAL
        # ======================
        frame_login = ctk.CTkFrame(
            self,
            width=400,
            height=350,
            corner_radius=15,
            fg_color="white"
        )
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            frame_login,
            text="Acesso ao Sistema",
            font=("Arial Black", 26, "bold"),
            text_color="#222"
        ).pack(pady=(25, 15))

        # Campo usuário
        ctk.CTkLabel(frame_login, text="Usuário:", text_color="#333").pack(anchor="w", padx=40, pady=(5, 0))
        self.login_entry = ctk.CTkEntry(frame_login, width=300, placeholder_text="Digite seu usuário")
        self.login_entry.pack(pady=5)

        # Campo senha
        ctk.CTkLabel(frame_login, text="Senha:", text_color="#333").pack(anchor="w", padx=40, pady=(5, 0))
        self.senha_entry = ctk.CTkEntry(frame_login, width=300, placeholder_text="Digite sua senha", show="•")
        self.senha_entry.pack(pady=5)

        # Botão de login
        ctk.CTkButton(
            frame_login,
            text="Entrar",
            width=200,
            height=45,
            fg_color="#2B8EFF",
            hover_color="#1E6FDA",
            corner_radius=8,
            command=self.verificar_login
        ).pack(pady=25)

        # Rodapé
        ctk.CTkLabel(
            frame_login,
            text="© 2025 Mecânica Masters",
            text_color="#888",
            font=("Arial", 10)
        ).pack(side="bottom", pady=10)

    # ======================
    # LÓGICA DE LOGIN
    # ======================
    def verificar_login(self):
        login = self.login_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not Metodos.campos_preenchidos(login, senha):
            Metodos.msg_aviso("Atenção", "Preencha usuário e senha!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT * FROM funcionarios
                WHERE login = ? AND senha = ?
            """, (login, senha))
            resultado = cursor.fetchone()

            if resultado:
                Metodos.msg_info("Sucesso", "Login realizado com sucesso!")
                self.after(150, self.abrir_tela_principal)  # ✅ executa com atraso seguro
            else:
                Metodos.msg_erro("Erro", "Usuário ou senha incorretos.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro de banco", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)






if __name__ == "__main__":
    app = TelaLogin()
    app.mainloop()
