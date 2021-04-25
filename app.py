from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from controllers.meuController import add_estudante

app = Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meudb.db'
db = SQLAlchemy(app)

class Estudante(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('nome', db.String(150))
    idade = db.Column('idade', db.Integer)

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


@app.route('/')
def index():
    estudantes = Estudante.query.all()
    return render_template('index.html', estudantes = estudantes)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        estudante = Estudante(request.form['nome'], request.form['idade'])
        # estudante = Estudante(data['nome'], data['idade'])
        db.session.add(estudante)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("add.html")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    estudante = Estudante.query.get(id)
    if request.method == 'POST':
        estudante.nome = request.form['nome']
        estudante.idade =  request.form['idade']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', estudante=estudante)

@app.route('/delete/<int:id>')
def delete(id):
    estudante = Estudante.query.get(id)
    db.session.delete(estudante)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run()