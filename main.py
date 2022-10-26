from flask import Flask, request, render_template
import requests

app = Flask(__name__, template_folder='www')


@app.route('/')
def home():
    return render_template("index.html", message="Indiquez l'ID du parking à vérifier.")


@app.route("/", methods=["POST"])
def places():
    reponse = requests.get(
        "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-parcsrelais-star-etat-tr&q=&facet=idparc&facet=nom&facet=etatouverture&facet=etatremplissage")
    data = reponse.json()
    records = data["records"]

    if int(request.form["text"]) - 1 > len(records):
        return render_template("index.html", message="Vous avez entré un ID inconnu, réessayez.")

    parkings = records[int(request.form["text"]) - 1]
    parking = parkings["fields"]
    if not parking['etatouverture'] == 'OUVERT':
        return render_template("index.html", message="Le parking " + str(parking['nom']) + "n'est pas ouvert.")
    return render_template("index.html", message="Il reste " + str(parking['nbplacessolistesdispo']) +
                                                 " places disponibles au parking " + str(parking['nom']) + " !")


if __name__ == "__main__":
    app.run()
