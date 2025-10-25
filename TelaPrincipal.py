import tkinter as tk
from Metodos import Metodos

class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TELA PRINCIPAL")
        self.geometry("600x400")
        self.resizable(False, False)

        tk.Label(self, text="TELA PRINCIPAL", font=("Arial", 18, "bold")).pack(pady=25)

        tk.Button(self, text="Produtos", width=30, command=self.abrir_tela_produto).pack(pady=10)
        tk.Button(self, text="Clientes", width=30, command=self.abrir_tela_cliente).pack(pady=10)
        tk.Button(self, text="Funcionários", width=30, command=self.abrir_tela_funcionario).pack(pady=10)
        tk.Button(self, text="Sair", width=30, bg="#d9534f", fg="white", command=self.destroy).pack(pady=25)

        self.mainloop()

    def abrir_tela_produto(self):
        self.destroy()
        from TelaProduto import TelaProduto  # 👈 import movido pra dentro
        TelaProduto()

    def abrir_tela_cliente(self):
        self.destroy()
        from TelaCliente import TelaCliente  # 👈 import movido pra dentro
        TelaCliente()

    def abrir_tela_funcionario(self):
        self.destroy()
        from TelaFuncionario import TelaFuncionario  # 👈 import movido pra dentro
        TelaFuncionario()
