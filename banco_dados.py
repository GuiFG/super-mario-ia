import sqlite3
import base64
import json


def criarTabela():
    conection = sqlite3.connect('mario.db')
    cursor = conection.cursor()

    cursor.execute("""
        CREATE TABLE agente (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            mente TEXT NOT NULL,
            mestre INTEGER NOT NULL,
            geracao INTEGER,
            pontuacao INTEGER NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE informacoes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            dados TEXT NOT NULL
        );
    """)

    conection.close()

def salvarAgente(mente, mestre, geracao, pontuacao):
    connection = sqlite3.connect("mario.db")
    cursor = connection.cursor()

    menteBytes = mente.encode("ascii")
    mente = base64.b64encode(menteBytes)

    pontuacao = int(pontuacao)

    print(pontuacao)
  
    cursor.execute("""
        INSERT INTO agente(mente, mestre, geracao, pontuacao)
        VALUES (?, ?, ?, ?)
    """, (mente, mestre, geracao, pontuacao))

    connection.commit()

    connection.close()

def getMenteMelhorAgente():
    connection = sqlite3.connect("mario.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, mente, mestre FROM agente
        ORDER BY pontuacao DESC, id DESC
    """)

    result = cursor.fetchall()

    if len(result) > 0:
        menteBytes = result[0][1]

        menteBytes = base64.b64decode(menteBytes)
        mente = menteBytes.decode("ascii")

        mente = json.loads(mente)

        connection.close()
        return mente

    connection.close()
    return {}

def getMenteMaiorPontuacao():
    connection = sqlite3.connect("mario.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, mente, mestre FROM agente
        WHERE mestre = 0
        ORDER BY pontuacao DESC, id DESC
    """)

    result = cursor.fetchall()

    if len(result) > 0:
        menteBytes = result[0][1]

        menteBytes = base64.b64decode(menteBytes)
        mente = menteBytes.decode("ascii")

        mente = json.loads(mente)

        connection.close()
        return mente

    connection.close()
    return {}

def recuperarMenteGeracao(geracao):
    connection = sqlite3.connect("mario.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, mente, geracao FROM agente
        WHERE geracao = ?
        ORDER BY id DESC
    """, (geracao,))

    result = cursor.fetchall()

    if (len(result) > 0):
        menteBytes = result[0][1]

        menteBytes = base64.b64decode(menteBytes)
        mente = menteBytes.decode("ascii")

        mente = json.loads(mente)

        connection.close()
        return mente

    connection.close()
    return {}

def salvarDados(dados):
    connection = sqlite3.connect("mario.db")
    cursor = connection.cursor()

    dadosBytes = dados.encode("ascii")
    dados = base64.b64encode(dadosBytes)

    cursor.execute("""
        INSERT INTO informacoes (dados)
        VALUES (?)
    """, (dados,))

    connection.commit()

    connection.close()

def recuperarDados():
    connection = sqlite3.connect("mario.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, dados FROM informacoes
        ORDER BY id DESC
    """)

    result = cursor.fetchall()

    if len(result) > 0:
        dados = result[0][1]

        dados = base64.b64decode(dados)
        dados = dados.decode("ascii")

        dados = json.loads(dados)

        connection.close()
        return dados
    
    connection.close()
    return {}

def main():
    criarTabela()

if __name__ == '__main__':
    main()