from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "greenplace_secret"


# =========================
# CONFIGURACIÓN BD
# =========================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# =========================
# MODELOS
# =========================
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)




class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)


# =========================
# RUTAS PRINCIPALES
# =========================
@app.route("/")
def index():
    return render_template("index.html")




@app.route("/inicio")
def inicio():
    return render_template("inicio.html")




@app.route("/reciclaje")
def reciclaje():
    return render_template("reciclaje.html")




@app.route("/manualidades")
def manualidades():
    return render_template("manualidades.html")




@app.route("/contaminacion")
def contaminacion():
    return render_template("contaminacion.html")




@app.route("/mapa")
def mapa():
    return render_template("mapa.html")




@app.route("/juego")
def juego():
    return render_template("juego.html")


# =========================
# COMENTARIOS (BD)
# =========================
@app.route("/comentarios", methods=["GET", "POST"])
def comentarios():
    if request.method == "POST":
        nombre = request.form["nombre"]
        mensaje = request.form["mensaje"]


        nuevo = Comentario(nombre=nombre, mensaje=mensaje)
        db.session.add(nuevo)
        db.session.commit()


        return redirect(url_for("comentarios"))


    comentarios = Comentario.query.all()
    return render_template("comentarios.html", comentarios=comentarios)


# ---  RUTA PARA BORRAR ---
@app.route("/borrar_comentario/<int:id>", methods=["POST"])
def borrar_comentario(id):
    comentario = Comentario.query.get_or_404(id) # Busca el comentario o lanza error 404
    db.session.delete(comentario) # Lo borra de la sesión
    db.session.commit() # Guarda los cambios en la base de datos
    return redirect(url_for("comentarios")) # Regresa a la página de comentarios
# ------------------------------


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]


        user = Usuario.query.filter_by(
            username=username,
            password=password
        ).first()


        if user:
            return redirect(url_for("inicio"))
        else:
            flash("Usuario o contraseña incorrectos")


    return render_template("login.html")


# =========================
# REGISTRO
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]


        existe = Usuario.query.filter_by(username=username).first()


        if existe:
            flash("Ese usuario ya existe")
        else:
            nuevo = Usuario(username=username, password=password)
            db.session.add(nuevo)
            db.session.commit()
            return redirect(url_for("login"))


    return render_template("registro.html")


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)