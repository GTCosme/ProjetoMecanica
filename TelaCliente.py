import tkinter as tk



class TelaCliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA CLIENTE")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Cliente", width=30, command=self.tela_cadastro_cliente).pack(pady=5)
        tk.Button(self, text="Consultar Cliente", width=30).pack(pady=5)
        tk.Button(self, text="Modificar Cliente", width=30).pack(pady=5)
        tk.Button(self, text="Voltar", width=30, command=self.voltar).pack(pady=25)

        self.mainloop()

    def tela_cadastro_cliente(self):
        self.limpar_tela()
        tk.Label(self, text="TELA CADASTRO CLIENTE", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Nome do Cliente:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Label(self, text="CPF:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Label(self, text="Telefone:").pack()
        tk.Entry(self, width=40).pack(pady=5)

        tk.Button(self, text="Salvar", width=15).pack(pady=15)
        tk.Button(self, text="Voltar", width=15, command=self.voltar_cliente).pack()

    def voltar(self):
        self.destroy()
        from TelaPrincipal import TelaPrincipal
        TelaPrincipal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def voltar_cliente(self):
        self.destroy()
        TelaCliente()