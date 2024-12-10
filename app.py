from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Conectar ao banco de dados SQLite
def get_db():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar as tabelas do banco de dados
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        );
    ''')
    conn.commit()
    conn.close()

# Endpoint para adicionar um novo produto
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    data = request.get_json()
    nome = data['nome']
    categoria = data['categoria']
    preco = data['preco']
    quantidade = data['quantidade']
    
    conn = get_db()
    conn.execute('''
        INSERT INTO produtos (nome, categoria, preco, quantidade)
        VALUES (?, ?, ?, ?)
    ''', (nome, categoria, preco, quantidade))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Produto adicionado com sucesso!'}), 201

# Endpoint para registrar entrada de produto
@app.route('/entrada', methods=['POST'])
def entrada_produto():
    data = request.get_json()
    produto_id = data['produto_id']
    quantidade = data['quantidade']
    
    conn = get_db()
    
    # Atualiza a quantidade do produto
    conn.execute('''
        UPDATE produtos
        SET quantidade = quantidade + ?
        WHERE id = ?
    ''', (quantidade, produto_id))
    
    # Registra a movimentação
    conn.execute('''
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, data)
        VALUES (?, 'entrada', ?, ?)
    ''', (produto_id, quantidade, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Entrada registrada com sucesso!'}), 201

# Endpoint para registrar saída de produto
@app.route('/saida', methods=['POST'])
def saida_produto():
    data = request.get_json()
    produto_id = data['produto_id']
    quantidade = data['quantidade']
    
    conn = get_db()
    
    # Atualiza a quantidade do produto
    conn.execute('''
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
    ''', (quantidade, produto_id))
    
    # Registra a movimentação
    conn.execute('''
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, data)
        VALUES (?, 'saida', ?, ?)
    ''', (produto_id, quantidade, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Saída registrada com sucesso!'}), 201

# Endpoint para listar produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = get_db()
    cursor = conn.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    
    result = []
    for produto in produtos:
        result.append({
            'id': produto['id'],
            'nome': produto['nome'],
            'categoria': produto['categoria'],
            'preco': produto['preco'],
            'quantidade': produto['quantidade']
        })
    
    return jsonify(result)

# Endpoint para listar movimentações
@app.route('/movimentacoes', methods=['GET'])
def listar_movimentacoes():
    conn = get_db()
    cursor = conn.execute('SELECT * FROM movimentacoes')
    movimentacoes = cursor.fetchall()
    conn.close()
    
    result = []
    for mov in movimentacoes:
        result.append({
            'id': mov['id'],
            'produto_id': mov['produto_id'],
            'tipo': mov['tipo'],
            'quantidade': mov['quantidade'],
            'data': mov['data']
        })
    
    return jsonify(result)

# Novo endpoint para gerar relatório completo (Produtos + Movimentações)
@app.route('/relatorio', methods=['GET'])
def gerar_relatorio():
    conn = get_db()
    
    # Recuperar todos os produtos com suas quantidades atuais
    cursor_produtos = conn.execute('SELECT * FROM produtos')
    produtos = cursor_produtos.fetchall()
    
    # Recuperar todas as movimentações realizadas
    cursor_movimentacoes = conn.execute('SELECT * FROM movimentacoes')
    movimentacoes = cursor_movimentacoes.fetchall()
    
    conn.close()
    
    # Gerar o relatório completo
    relatorio = {
        'produtos': [],
        'movimentacoes': []
    }
    
    for produto in produtos:
        relatorio['produtos'].append({
            'id': produto['id'],
            'nome': produto['nome'],
            'categoria': produto['categoria'],
            'preco': produto['preco'],
            'quantidade': produto['quantidade']
        })
    
    for movimentacao in movimentacoes:
        relatorio['movimentacoes'].append({
            'id': movimentacao['id'],
            'produto_id': movimentacao['produto_id'],
            'tipo': movimentacao['tipo'],
            'quantidade': movimentacao['quantidade'],
            'data': movimentacao['data']
        })
    
    return jsonify(relatorio)

if __name__ == '__main__':
    init_db()  # Cria as tabelas ao iniciar
    app.run(debug=True)
