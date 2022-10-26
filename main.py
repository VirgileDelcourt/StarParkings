import requests
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')


def places_libres(ID_parking: int):
    reponse = requests.get(
        "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-parcsrelais-star-etat-tr&q=&facet=idparc&facet=nom&facet=etatouverture&facet=etatremplissage")
    data = reponse.json()
    records = data["records"]
    if not (1 <= ID_parking <= len(records)):
        raise ValueError(f"Le parking n° {ID_parking} est inconnu")
    parkings = records[ID_parking - 1]
    parking = parkings["fields"]
    return parking


@app.route('/')
def home():
    return render_template("index.html", message="Indiquez l'ID du parking à vérifier.")


@app.route("/", methods=["POST"])
def places_html():
    if request.form["text"] == "":
        return render_template("index.html", message="Vous avez entré un ID inconnu, réessayez.")

    id_parking = int(request.form["text"])

    try:
        parking = places_libres(id_parking)
    except ValueError as err:
        return render_template("index.html", message=f"Erreur : {err}")

    if not parking['etatouverture'] == 'OUVERT':
        return render_template("index.html", message="Le parking " + str(parking['nom']) + "n'est pas ouvert.")

    return render_template(
        "index.html",
        message=f"Il reste {parking['nbplacessolistesdispo']} places disponibles au parking {parking['nom']} !",
        classe="alert" if parking['nbplacessolistesdispo'] <= 20 else None,
        info_parking=parking,
        id_parking=id_parking,
    )


@app.route("/parking/<int:id_parking>", methods=["GET"])
def places_json(id_parking: int):
    return places_libres(id_parking)


if __name__ == "__main__":
    app.run()
