import folium
from folium import PolyLine, CircleMarker
from folium.plugins import MarkerCluster
import webbrowser

# ---- 1. Coordonnées GPS de 10 communes ----
communes = {
    "Gombe": (-4.303056, 15.303333),
    "Ngaliema": (-4.369733, 15.256448),
    "Kintambo": (-4.326983, 15.272884),
    "Limete": (-4.464167, 15.348889),
    "Lemba": (-4.408056, 15.326111),
    "Masina": (-4.392778, 15.400556),
    "Matete": (-4.399167, 15.337500),
    "Barumbu": (-4.312500, 15.293611),
    "Bandalungwa": (-4.366111, 15.280556),
    "Ngiri-Ngiri": (-4.386111, 15.319444)
}

# ---- 2. Centre de la carte ----
avg_lat = sum(lat for lat, lon in communes.values()) / len(communes)
avg_lon = sum(lon for lat, lon in communes.values()) / len(communes)

# ---- 3. Création de la carte OpenStreetMap ----
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, tiles="OpenStreetMap")

# ---- 4. Couleurs pour chaque commune ----
couleurs = [
    "blue", "green", "purple", "orange", "darkred",
    "cadetblue", "darkgreen", "darkpurple", "pink", "lightblue"
]

# ---- 5. Ajout des marqueurs avec couleurs ----
cluster = MarkerCluster().add_to(m)

for (nom, (lat, lon)), couleur in zip(communes.items(), couleurs):
    CircleMarker(
        location=[lat, lon],
        radius=7,
        color=couleur,
        fill=True,
        fill_color=couleur,
        fill_opacity=0.8,
        popup=f"<b>{nom}</b><br>Latitude : {lat}<br>Longitude : {lon}"
    ).add_to(m)
    
    folium.Marker(
        location=[lat, lon],
        tooltip=nom
    ).add_to(cluster)

# ---- 6. Lignes de différentes couleurs pour "directions" ----
lignes = [
    (["Gombe", "Kintambo"], "blue"),
    (["Ngaliema", "Bandalungwa"], "green"),
    (["Limete", "Masina"], "purple"),
    (["Matete", "Lemba"], "orange")
]

for communes_ligne, couleur in lignes:
    coords = [communes[c] for c in communes_ligne]
    PolyLine(coords, color=couleur, weight=3, opacity=0.8).add_to(m)

# ---- 7. Ligne rouge courte pour le "chemin le plus court" ----
# Ici on relie seulement Gombe et Limete pour que ce soit clair
PolyLine([communes["Gombe"], communes["Limete"]], color="red", weight=5, opacity=0.9).add_to(m)

# ---- 8. Sauvegarde et ouverture automatique ----
fichier = "carte_kinshasa_10_communes.html"
m.save(fichier)
print(f"Carte générée : {fichier}")
webbrowser.open(fichier)
