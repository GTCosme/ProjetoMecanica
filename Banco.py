import sqlite3

conn = sqlite3.connect('mecanica_master.db')

conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
cpf INTEGER PRIMARY KEY,
nome TEXT NOT NULL,
email TEXT NOT NULL,
telefone TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS funcionarios (
cpf INTEGER PRIMARY KEY,
nome TEXT NOT NULL,
login TEXT NOT NULL,
senha TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
tipoProduto TEXT NOT NULL,
preco FLOAT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS servicos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
servico TEXT NOT NULL,
preco FLOAT NOT NULL,
funcionarioResposavel TEXT NOT NULL,
FOREIGN KEY (funcionarioResponsavel) REFERENCES funcionarios (nome)
);
''')

conn.commit()
conn.close()