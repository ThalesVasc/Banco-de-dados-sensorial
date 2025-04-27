from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuração do banco (agora SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analise.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Modelos
class Analise(db.Model):
    __tablename__ = 'analises'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    responsavel = db.Column(db.String(255), nullable=False)
    data = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    tipo_avaliacao = db.Column(db.String(255), nullable=False)
    intencao_compra = db.Column(db.String(255), nullable=False)
    amostras = db.relationship('Amostra', backref='analise', cascade="all, delete-orphan", lazy=True)


class Amostra(db.Model):
    __tablename__ = 'amostras'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    analise_id = db.Column(db.Integer, db.ForeignKey('analises.id'), nullable=False)


# Rotas
@app.route('/')
def index():
    analises = Analise.query.all()
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

        nova_analise = Analise(
            nome=nome,
            responsavel=responsavel,
            data=data,
            status=status,
            tipo_avaliacao=tipo,
            intencao_compra=intencao
        )
        db.session.add(nova_analise)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('nova_analise.html')


@app.route('/analise/<int:id>/amostras')
def amostras(id):
    amostras = Amostra.query.filter_by(analise_id=id).all()
    return render_template('amostras.html', amostras=amostras, analise_id=id)


@app.route('/analise/<int:id>/nova_amostra', methods=['GET', 'POST'])
def nova_amostra(id):
    if request.method == 'POST':
        descricao = request.form['descricao']
        nova_amostra = Amostra(
            descricao=descricao,
            analise_id=id
        )
        db.session.add(nova_amostra)
        db.session.commit()
        return redirect(url_for('amostras', id=id))

    return render_template('nova_amostra.html', analise_id=id)


@app.route('/analise/<int:id>/detalhes')
def detalhes_analise(id):
    analise = Analise.query.get_or_404(id)
    amostras = Amostra.query.filter_by(analise_id=id).all()
    return render_template('detalhes_analise.html', analise=analise, amostras=amostras)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem
    app.run(debug=True)
