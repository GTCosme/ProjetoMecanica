import tkinter as tk

class TelaProduto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA PRODUTO")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Produto", width=30, command=self.tela_cadastro_produto).pack(pady=5)
        tk.Button(self, text="Consultar Quantidade", width=30).pack(pady=5)
        tk.Button(self, text="Modificar Produto", width=30).pack(pady=5)
        tk.Button(self, text="Voltar", width=30, command=self.voltar).pack(pady=25)

        self.mainloop()

    def tela_cadastro_produto(self):
        self.limpar_tela()
        tk.Label(self, text="TELA CADASTRO PRODUTO", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Nome do Produto:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Label(self, text="Quantidade:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Label(self, text="Preço:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Button(self, text="Salvar", width=15).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.__init__).pack()

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal  # ⬅️ importa aqui dentro!
        TelaPrincipal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()
