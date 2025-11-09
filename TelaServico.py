import customtkinter as ctk
from PIL import Image
import sqlite3
from tkinter import ttk, messagebox
from Metodos import Metodos


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# =================== TELA PRINCIPAL SERVIÇO ===================
class TelaServico(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mecânica Masters - Serviços")
        self.geometry("1000x600")
        self.resizable(False, False)


        # =================== NAVBAR ===================
        navbar = ctk.CTkFrame(self, height=60, fg_color="#F8F9FA")
        navbar.pack(fill="x", side="top")

        logo_nav = ctk.CTkImage(light_image=Image.open("img/logo.png"), size=(40, 40))
        ctk.CTkLabel(navbar, image=logo_nav, text="").pack(side="left", padx=20)

        botoes_menu = [
            ("Tela inicial", self.voltar_tela_inicial),
            ("Produtos", self.abrir_tela_produto),
            ("Serviços", lambda: None),
            ("Funcionários", self.abrir_tela_funcionario),
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

        ctk.CTkLabel(frame, text="Gerenciamento de Serviços",
                     font=("Arial Black", 28, "bold"), text_color="#222").pack(pady=(80, 30))

        botoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        botoes_frame.pack(pady=40)

        ctk.CTkButton(botoes_frame, text="Cadastrar Serviço",
                      width=200, height=45,
                      fg_color="black", text_color="white",
                      hover_color="#333",
                      command=self.abrir_cadastro).pack(side="left", padx=15)

        ctk.CTkButton(botoes_frame, text="Consultar Serviço",
                      width=200, height=45,
                      fg_color="white", text_color="black",
                      hover_color="#E1E1E1",
                      command=self.abrir_consultar).pack(side="left", padx=15)

        ctk.CTkButton(botoes_frame, text="Modificar Serviço",
                      width=200, height=45,
                      fg_color="black", text_color="white",
                      hover_color="#333",
                      command=self.abrir_modificar).pack(side="left", padx=15)

        self.mainloop()

    # =================== NAVEGAÇÃO ===================
    def abrir_cadastro(self):
        self.destroy()
        CadastroServico()

    def abrir_consultar(self):
        self.destroy()
        ConsultarServico()

    def abrir_modificar(self):
        self.destroy()
        ModificarServico()

    def voltar_tela_inicial(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal().mainloop()

    def abrir_tela_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto
        TelaProduto()

    def abrir_tela_funcionario(self):
        self.destroy()
        from TelaFuncionario import TelaFuncionario
        TelaFuncionario()

    def abrir_tela_cliente(self):
        self.destroy()
        from TelaCliente import TelaCliente
        TelaCliente()


# =================== CADASTRAR SERVIÇO ===================
class CadastroServico(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cadastrar Serviço")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Cadastrar Serviço", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_id = Metodos.criar_entry(frame, "ID:")
        self.entry_servico = Metodos.criar_entry(frame, "Serviço:")
        self.entry_preco = Metodos.criar_entry(frame, "Preço:")
        self.entry_preco.bind("<FocusOut>", lambda e: Metodos.formatar_moeda(self.entry_preco))

        ctk.CTkLabel(frame, text="Funcionário Responsável:").pack()
        self.combo_funcionario = ttk.Combobox(frame, width=37, state="readonly")
        self.combo_funcionario.pack(pady=5)
        self.carregar_funcionarios()

        ctk.CTkButton(frame, text="Salvar", width=200, height=40, command=self.salvar).pack(pady=20)
        ctk.CTkButton(frame, text="Voltar", width=200, height=40,
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
            ("Serviços", self.voltar),
            ("Funcionários", self.abrir_tela_funcionario),
            ("Clientes", self.abrir_tela_cliente)
        ]

        for texto, cmd in botoes:
            ctk.CTkButton(navbar, text=texto, command=cmd,
                          fg_color="transparent", hover_color="#E1E1E1",
                          text_color="#222", font=("Arial", 13, "bold"),
                          width=100, height=35).pack(side="left", padx=4)

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
        id_serv = self.entry_id.get().strip()
        servico = self.entry_servico.get().strip()
        preco = self.entry_preco.get().strip()
        funcionario = self.combo_funcionario.get().strip()

        if not Metodos.campos_preenchidos(id_serv, servico, preco, funcionario):
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
            """, (id_serv, servico, preco, funcionario))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Serviço cadastrado com sucesso!")
            Metodos.limpar_campos(self.entry_id, self.entry_servico, self.entry_preco)
            self.combo_funcionario.set("")
        except sqlite3.IntegrityError:
            Metodos.msg_erro("Erro", "ID já cadastrado.")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def voltar(self):
        self.destroy()
        TelaServico()

    # Navegação comum
    def voltar_tela_inicial(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()

    def abrir_tela_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto
        TelaProduto()

    def abrir_tela_funcionario(self):
        from TelaFuncionario import TelaFuncionario
        self.destroy()
        TelaFuncionario().mainloop()

    def abrir_tela_cliente(self):
        self.destroy()
        from TelaCliente import TelaCliente
        TelaCliente()


# =================== CONSULTAR SERVIÇO ===================
class ConsultarServico(CadastroServico):
    def __init__(self):
        super().__init__()
        self.title("Consultar Serviço")
        Metodos.limpar_tela(self)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Consultar Serviço", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_id = Metodos.criar_entry(frame, "Digite o ID do Serviço:")
        ctk.CTkButton(frame, text="Consultar", width=200, height=40, command=self.consultar).pack(pady=15)

        self.frame_resultado = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_resultado.pack(pady=10)

        ctk.CTkButton(frame, text="Voltar", width=200, height=40,
                      fg_color="#6c757d", command=self.voltar).pack()

    def consultar(self):
        for w in self.frame_resultado.winfo_children():
            w.destroy()

        id_serv = self.entry_id.get().strip()
        if not id_serv:
            ctk.CTkLabel(self.frame_resultado, text="Digite o ID!", text_color="red").pack()
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT servico, preco, funcionarioResponsavel FROM servicos WHERE id = ?", (id_serv,))
            resultado = cursor.fetchone()
            if resultado:
                ctk.CTkLabel(self.frame_resultado, text=f"Serviço: {resultado[0]}").pack(anchor="w")
                ctk.CTkLabel(self.frame_resultado, text=f"Preço: {resultado[1]}").pack(anchor="w")
                ctk.CTkLabel(self.frame_resultado, text=f"Funcionário: {resultado[2]}").pack(anchor="w")
            else:
                ctk.CTkLabel(self.frame_resultado, text="Serviço não encontrado.", text_color="red").pack()
        except sqlite3.Error as erro:
            ctk.CTkLabel(self.frame_resultado, text=f"Erro: {erro}", text_color="red").pack()
        finally:
            Metodos.fechar(conexao)


# =================== MODIFICAR SERVIÇO ===================
class ModificarServico(CadastroServico):
    def __init__(self):
        super().__init__()
        self.title("Modificar Serviço")
        Metodos.limpar_tela(self)

        self.criar_navbar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Modificar Serviço", font=("Arial Black", 26, "bold")).pack(pady=(60, 20))

        self.entry_id = Metodos.criar_entry(frame, "Digite o ID do Serviço:")
        ctk.CTkButton(frame, text="Buscar Serviço", width=200, height=40,
                      command=self.buscar_servico).pack(pady=15)

        self.frame_edicao = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_edicao.pack(pady=10)

        ctk.CTkButton(frame, text="Voltar", width=200, height=40,
                      fg_color="#6c757d", command=self.voltar).pack()

    def buscar_servico(self):
        for w in self.frame_edicao.winfo_children():
            w.destroy()

        id_serv = self.entry_id.get().strip()
        if not id_serv:
            Metodos.msg_aviso("Atenção", "Digite o ID!")
            return

        conexao = Metodos.conectar()
        if not conexao:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT servico, preco, funcionarioResponsavel FROM servicos WHERE id = ?", (id_serv,))
            servico = cursor.fetchone()

            if servico:
                self.entry_servico = Metodos.criar_entry(self.frame_edicao, "Serviço:", servico[0])
                self.entry_preco = Metodos.criar_entry(self.frame_edicao, "Preço:", servico[1])

                ctk.CTkLabel(self.frame_edicao, text="Funcionário Responsável:").pack()
                self.combo_funcionario = ttk.Combobox(self.frame_edicao, width=37, state="readonly")
                self.combo_funcionario.pack(pady=5)
                self.carregar_funcionarios()
                self.combo_funcionario.set(servico[2])

                ctk.CTkButton(self.frame_edicao, text="Salvar Alterações",
                              width=200, height=40, command=lambda: self.salvar_alteracoes(id_serv)).pack(pady=10)

                ctk.CTkButton(self.frame_edicao, text="Excluir Serviço",
                              width=200, height=40, fg_color="#dc3545",
                              hover_color="#b02a37",
                              command=lambda: self.excluir_servico(id_serv)).pack(pady=5)
            else:
                Metodos.msg_info("Aviso", "Serviço não encontrado!")
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Ocorreu um erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def salvar_alteracoes(self, id_serv):
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
                SET servico=?, preco=?, funcionarioResponsavel=?
                WHERE id=?
            """, (servico, preco, funcionario, id_serv))
            conexao.commit()
            Metodos.msg_info("Sucesso", "Serviço atualizado com sucesso!")
            self.voltar()
        except sqlite3.Error as erro:
            Metodos.msg_erro("Erro", f"Erro: {erro}")
        finally:
            Metodos.fechar(conexao)

    def excluir_servico(self, id_serv):
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
            Metodos.msg_erro("Erro", f"Erro ao excluir: {erro}")
        finally:
            Metodos.fechar(conexao)


if __name__ == "__main__":
    TelaServico()
