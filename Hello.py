from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home")
def home():
    return "<p>Bienvenue sur la page d'accueil !</p><p><a href='/presentation'>Voir la présentation</a></p>"


@app.route("/presentation")
def presentation():
    nom = "Jean"
    age = 30
    profession = "Développeur"
    interets = ["Programmation", "Musique", "Voyages"]
    return render_template("presentation.html", nom=nom, age=age, profession=profession, interets=interets)

if __name__ == "__main__":
    app.run(debug=True)
