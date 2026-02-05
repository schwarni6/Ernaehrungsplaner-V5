import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Ernährungsplan Pro+", page_icon="🥗", layout="wide")
st.title("🥗 7-Tage Ernährungsplan Generator PRO+")

# ========== SIDEBAR ==========
st.sidebar.header("👤 Profil")

geschlecht = st.sidebar.selectbox("Geschlecht", ["Männlich", "Weiblich"])
alter = st.sidebar.number_input("Alter", 14, 100, 30)
gewicht = st.sidebar.number_input("Gewicht (kg)", 40, 200, 75)
groesse = st.sidebar.number_input("Größe (cm)", 140, 220, 175)

aktivitaet = st.sidebar.selectbox(
    "Aktivitätslevel",
    ["Wenig Bewegung", "Leicht aktiv", "Mittel aktiv", "Sehr aktiv"]
)

ziel = st.sidebar.selectbox(
    "Ziel",
    ["Abnehmen", "Gewicht halten", "Zunehmen", "Muskelaufbau"]
)

ernaehrung = st.sidebar.selectbox(
    "Ernährungsform",
    ["Normal", "Vegan"]
)

allergien = st.sidebar.multiselect(
    "🚫 Allergien / Unverträglichkeiten",
    ["Nüsse", "Laktose", "Gluten", "Soja"]
)

mahlzeiten = st.sidebar.slider("Mahlzeiten pro Tag", 3, 6, 4)

# ========== KALORIEN ==========
faktoren = {
    "Wenig Bewegung": 1.2,
    "Leicht aktiv": 1.375,
    "Mittel aktiv": 1.55,
    "Sehr aktiv": 1.725
}

if geschlecht == "Männlich":
    bmr = 10 * gewicht + 6.25 * groesse - 5 * alter + 5
else:
    bmr = 10 * gewicht + 6.25 * groesse - 5 * alter - 161

kalorien = int(bmr * faktoren[aktivitaet])

if ziel == "Abnehmen":
    kalorien -= 500
elif ziel == "Zunehmen":
    kalorien += 300
elif ziel == "Muskelaufbau":
    kalorien += 400

# ========== MAKROS ==========
if ziel == "Muskelaufbau":
    protein_ratio = 0.35
else:
    protein_ratio = 0.30

protein = int((kalorien * protein_ratio) / 4)
carbs = int((kalorien * 0.45) / 4)
fat = int((kalorien * (1 - protein_ratio - 0.45)) / 9)

# ========== GERICHTE ==========
foods = {
    "Normal": [
        {"name": "Haferflocken mit Beeren", "tags": [], "p": 20, "kcal": 450},
        {"name": "Rührei mit Vollkornbrot", "tags": ["Gluten"], "p": 30, "kcal": 500},
        {"name": "Skyr mit Honig", "tags": ["Laktose"], "p": 25, "kcal": 300},
        {"name": "Hähnchen mit Reis", "tags": [], "p": 45, "kcal": 650},
        {"name": "Rindersteak mit Kartoffeln", "tags": [], "p": 50, "kcal": 700},
        {"name": "Lachs mit Quinoa", "tags": [], "p": 40, "kcal": 680},
        {"name": "Pasta Bolognese", "tags": ["Gluten"], "p": 35, "kcal": 750},
        {"name": "Omelette mit Gemüse", "tags": [], "p": 35, "kcal": 480},
        {"name": "Wrap mit Hähnchen", "tags": ["Gluten"], "p": 40, "kcal": 600},
        {"namimport streamlit as st
import random
import pandas as pde": "Protein Pancakes", "tags": ["Gluten", "Laktose"], "p": 30, "kcal": 520},
        {"name": "Nüsse", "tags": ["Nüsse"], "p": 6, "kcal": 180},
        {"name": "Apfel", "tags": [], "p": 0, "kcal": 95},
        {"name": "Proteinriegel", "tags": ["Laktose"], "p": 20, "kcal": 250}
    ],

    "Vegan": [
        {"name": "Porridge mit Mandelmilch", "tags": ["Nüsse"], "p": 15, "kcal": 420},
        {"name": "Smoothie Bowl", "tags": [], "p": 12, "kcal": 400},
        {"name": "Tofu mit Reis", "tags": ["Soja"], "p": 30, "kcal": 600},
        {"name": "Kichererbsen-Curry", "tags": [], "p": 22, "kcal": 650},
        {"name": "Linsen-Dal", "tags": [], "p": 25, "kcal": 620},
        {"name": "Vegane Wraps", "tags": ["Gluten"], "p": 20, "kcal": 550},
        {"name": "Gemüsepfanne mit Reis", "tags": [], "p": 18, "kcal": 580},
        {"name": "Falafel Bowl", "tags": ["Gluten"], "p": 24, "kcal": 630},
        {"name": "Veganes Chili sin Carne", "tags": [], "p": 28, "kcal": 660},
        {"name": "Hummus mit Vollkornbrot", "tags": ["Gluten"], "p": 16, "kcal": 500}
    ]
}

# ========== FILTER NACH ALLERGIEN ==========
verfuegbare_gerichte = [
    f for f in foods[ernaehrung]
    if not any(tag in allergien for tag in f["tags"])
]

if len(verfuegbare_gerichte) == 0:
    st.error("⚠️ Keine passenden Gerichte wegen deiner Allergien gefunden!")
    st.stop()

# ========== BUTTON ==========
if st.button("🚀 7-Tage-Plan generieren"):

    tage = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]

    st.subheader("📊 Deine Ziele")
    st.write(f"**Kalorien pro Tag:** {kalorien} kcal")
    st.write(f"**Protein:** {protein} g | **Carbs:** {carbs} g | **Fett:** {fat} g")

    st.subheader("📅 Dein 7-Tage-Plan")

    for tag in tage:
        st.markdown(f"### 🍽️ **{tag}**")

        plan = random.sample(
            verfuegbare_gerichte,
            k=min(mahlzeiten, len(verfuegbare_gerichte))
        )

        df = pd.DataFrame(plan)[["name", "kcal", "p"]]
        df.columns = ["Gericht", "Kalorien", "Protein (g)"]

        st.dataframe(df, use_container_width=True)

    st.success("✅ 7-Tage-Plan erfolgreich erstellt!")

else:
    st.info("👉 Drücke auf **'7-Tage-Plan generieren'**, wenn du fertig bist mit den Einstellungen.")
