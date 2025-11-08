import sqlite3
import tkinter as tk
from tkinter import messagebox
import re

class Metodos:
    DB_PATH = "mecanica_master.db"

    # ---------- Conexão com Banco ----------
    @staticmethod
    def conectar():
        try:
            conexao = sqlite3.connect(Metodos.DB_PATH)
            return conexao
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de Banco", f"Ocorreu um erro ao conectar: {erro}")
            return None

    # ---------- Fechar conexão (segurança) ----------
    @staticmethod
    def fechar(conexao):
        try:
            if conexao:
                conexao.close()
        except Exception:
            pass

    # ---------- Limpar Campos ----------
    @staticmethod
    def limpar_campos(*entries):
        for entry in entries:
            try:
                entry.delete(0, tk.END)
            except Exception:
                pass

    # ---------- Limpar Tela ----------
    @staticmethod
    def limpar_tela(tela):
        for widget in tela.winfo_children():
            widget.destroy()

    # ---------- Formatar CPF ----------
    @staticmethod
    def formatar_cpf(entry):
        texto = entry.get()
        texto = ''.join(filter(str.isdigit, texto))
        novo = ""

        if len(texto) >= 1:
            novo += texto[:3]
        if len(texto) > 3:
            novo = texto[:3] + '.' + texto[3:6]
        if len(texto) > 6:
            novo = texto[:3] + '.' + texto[3:6] + '.' + texto[6:9]
        if len(texto) > 9:
            novo = texto[:3] + '.' + texto[3:6] + '.' + texto[6:9] + '-' + texto[9:11]

        novo = novo[:14]
        entry.delete(0, tk.END)
        entry.insert(0, novo)

    # ---------- Formatar Telefone ----------
    @staticmethod
    def formatar_telefone(entry):
        texto = entry.get()
        texto = ''.join(filter(str.isdigit, texto))
        novo = texto
        if len(texto) > 2:
            ddd = texto[:2]
            resto = texto[2:]
            if len(resto) > 5:
                novo = f"({ddd}) {resto[:5]}-{resto[5:9]}"
            else:
                novo = f"({ddd}) {resto}"
        entry.delete(0, tk.END)
        entry.insert(0, novo[:15])

    # ---------- Validações ----------
    @staticmethod
    def campos_preenchidos(*valores):
        return all(v is not None and str(v).strip() != "" for v in valores)

    @staticmethod
    def validar_email(email):
        if not email:
            return False
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email) is not None

    @staticmethod
    def formatar_moeda(entry):
        texto = entry.get()
        if not texto:
            return
        # Remove qualquer caractere que não seja número ou ponto/virgula
        texto = texto.replace("R$", "").replace(".", "").replace(",", ".").strip()
        try:
            valor = float(texto)
            # Formata Moeda
            valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            entry.delete(0, tk.END)
            entry.insert(0, valor_formatado)
        except ValueError:
            entry.delete(0, tk.END)
            entry.insert(0, "R$ 0,00")

    # ---------- Mensagens ----------
    @staticmethod
    def msg_erro(titulo, msg):
        messagebox.showerror(titulo, msg)

    @staticmethod
    def msg_info(titulo, msg):
        messagebox.showinfo(titulo, msg)

    @staticmethod
    def msg_aviso(titulo, msg):
        messagebox.showwarning(titulo, msg)

    # ---------- Criar Entry ----------
    @staticmethod
    def criar_entry(pai, texto_label, valor_inicial=""):
        """Cria um Label e Entry dentro do pai e retorna o Entry"""
        tk.Label(pai, text=texto_label).pack()
        entry = tk.Entry(pai, width=40)
        entry.pack(pady=5)
        entry.insert(0, valor_inicial)
        return entry
