from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aurabank.db'
db = SQLAlchemy(app)


#rotas
@app.route("/")
def paginaprincipal():
    return render_template("homepage.html")

@app.route("/dashboard")
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for("paginaprincipal"))
    usuario = Usuario.query.get(session['usuario_id'])
    return render_template("dashboard.html", usuario=usuario)



class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    identificador = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    saldo = db.Column(db.Float, default=100.0) # Já começa com R$ 100 para testar!
    limite_credito = db.Column(db.Float, default=100.0)
    fatura = db.Column(db.Float, default=0.0)
with app.app_context():
    db.create_all()

from gerenciamento import *


if __name__ == "__main__":
    app.run(debug=True)

app.secret_key = 'qualquer_texto_secreto_aqui'
