#Participantes: Luan Moura, Gabriel da Silva, Barbara Lopes, Beatriz, Lucas Menezes,
# Anna Gabriela, Franciane e Eduardo Henrique
#Turma: 3C


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    idade = db.Column(db.Integer)
    cidade = db.Column(db.String)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def inicio():
    return render_template('index.html')

@app.route("/users")
def lista_cadastros():
    users = db.session.execute(db.select(Pessoa).order_by(Pessoa.username)).scalars()
    return render_template("user/lista.html", users=users)

@app.route("/users/create", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        user = Pessoa(
            username=request.form["username"],
            email=request.form["email"],
            idade=request.form["idade"],
            cidade=request.form["cidade"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("relatorio_info", id=user.id))

    return render_template("user/beijaflor.html")

@app.route("/user/<int:id>")
def relatorio_info(id):
    user = db.get_or_404(Pessoa, id)
    return render_template("user/detalhe.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def deletar(id):
    user = db.get_or_404(Pessoa, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("lista_cadastros"))

    return render_template("user/deletar.html", user=user)



if __name__ == '__main__':
    app.run(debug=True)
