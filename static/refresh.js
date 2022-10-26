function placesParkings (id_parking){
    if (!id_parking) {
        return
    }
    fetch(`http://localhost:5000/parking/${id_parking}`, {
        method: 'GET'
    })
    .then((response) => response.json())
    .then(function(data) {
        // console.info(`Nombre de places disponibles : ${data.nbplacessolistesdispo}. (mis à jour à ${data.lastupdate})`)
        document.getElementById("placesDispo").textContent=data.nbplacessolistesdispo
        document.getElementById("nomParking").textContent=data.nom
    })
   }

setInterval(function() {
    const id_parking = document.getElementById('id_parking').textContent
    placesParkings(id_parking)
}, 2 * 1000)

