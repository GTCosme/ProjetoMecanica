import tkinter as tk


class TelaFuncionario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA FUNCIONÁRIO")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Funcionário", width=30, command=self.tela_cadastro_funcionario).pack(pady=5)
        tk.Button(self, text="Modificar Funcionário", width=30).pack(pady=5)
        tk.Button(self, text="Voltar", width=30, command=self.voltar).pack(pady=25)

        self.mainloop()

    def tela_cadastro_funcionario(self):
        self.limpar_tela()
        tk.Label(self, text="TELA CADASTRO FUNCIONÁRIO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Nome do Funcionário:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Label(self, text="Cargo:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Label(self, text="Salário:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Button(self, text="Salvar", width=15).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.__init__).pack()

    def voltar(self):
        self.destroy()
        TelaPrincipal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()
