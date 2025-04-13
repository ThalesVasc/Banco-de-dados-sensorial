from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuração do banco
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="analise"
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM analises")
    analises = cursor.fetchall()
    return render_template('index.html', analises=analises)

@app.route('/nova', methods=['GET', 'POST'])
def nova_analise():
    if request.method == 'POST':
        nome = request.form['nome']
        responsavel = request.form['responsavel']
        data = request.form['data']
        status = request.form['status']
        tipo = request.form['tipo']
        intencao = request.form['intencao']

        cursor.execute("""
            INSERT INTO analises (nome, responsavel, data, status, tipo_avaliacao, intencao_compra)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, responsavel, data, status, tipo, intencao))
        db.commit()
        return redirect(url_for('index'))
    
    return render_template('nova_analise.html')

@app.route('/analise/<int:id>/amostras')
def amostras(id):
    cursor.execute("SELECT * FROM amostras WHERE analise_id = %s", (id,))
    amostras = cursor.fetchall()
    return render_template('amostras.html', amostras=amostras, analise_id=id)

@app.route('/analise/<int:id>/nova_amostra', methods=['GET', 'POST'])
def nova_amostra(id):
    if request.method == 'POST':
        descricao = request.form['descricao']
        cursor.execute("INSERT INTO amostras (analise_id, descricao) VALUES (%s, %s)", (id, descricao))
        db.commit()
        return redirect(url_for('amostras', id=id))
    
    return render_template('nova_amostra.html', analise_id=id)

@app.route('/analise/<int:id>/detalhes')
def detalhes_analise(id):
    # Buscar detalhes da análise
    cursor.execute("SELECT * FROM analises WHERE id = %s", (id,))
    analise = cursor.fetchone()

    # Buscar amostras relacionadas
    cursor.execute("SELECT * FROM amostras WHERE analise_id = %s", (id,))
    amostras = cursor.fetchall()

    # Passar os dados para o template
    return render_template('detalhes_analise.html', analise=analise, amostras=amostras)

if __name__ == '__main__':
    app.run(debug=True)