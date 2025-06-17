import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import requests

# Configurar la página
st.set_page_config(layout="wide")
st.title("Mapa de Centros Educativos en Valencia")

# --- Función para cargar datos desde la API ---
@st.cache_data
def cargar_centros():
    url = "https://tb-tallerdatafullstack.onrender.com/colegios"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("No se pudo cargar la información de los centros.")
        return pd.DataFrame()

# --- Cargar datos ---
df = cargar_centros()

# --- Layout en 3 columnas ---
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

# --- Columna 1: Filtros ---
with col1:
    st.subheader("🔎 Filtros")

    municipios = ['Todos'] + sorted(df['municipio'].dropna().unique().tolist())
    regimenes = ['Todos'] + sorted(df['regimen'].dropna().unique().tolist())

    municipio = st.selectbox("Municipio", municipios)
    print(municipio)
    regimen = st.selectbox("Tipo de centro", regimenes)
    print(regimen)

# --- Filtrar dataframe ---
if municipio != 'Todos':
    df = df[df['municipio'] == municipio]
if regimen != 'Todos':
    df = df[df['regimen'] == regimen]

# --- Columna 2: Mapa ---
with col2:
    st.subheader("🗺️ Mapa de centros")

    m = folium.Map(location=[39.47, -0.38], zoom_start=12)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=row["nombre"],
            icon=folium.Icon(color="blue", icon="graduation-cap", prefix="fa")
        ).add_to(m)

    mapa_data = st_folium(m, width=800, height=500)

# --- Columna 3: Detalles del centro ---
with col3:
    st.subheader("🏫 Información del centro")

    if mapa_data and mapa_data.get("last_object_clicked"):
        lat = mapa_data["last_object_clicked"]["lat"]
        lon = mapa_data["last_object_clicked"]["lng"]

        centro = df[(df["latitude"] == lat) & (df["longitude"] == lon)]

        if not centro.empty:
            c = centro.iloc[0]
            st.markdown(f"**Nombre:** {c['nombre']}")
            st.markdown(f"**Dirección:** {c['direccion']}")
            st.markdown(f"**Municipio:** {c['municipio']}")
            st.markdown(f"**Provincia:** {c['provincia']}")
            st.markdown(f"**CP:** {c['CP']}")
            st.markdown(f"**Régimen:** {c['regimen']}")
            st.markdown(f"**Teléfono:** {c['telef']}")
            st.markdown(f"**Email:** {c['mail']}")
        else:
            st.write("No se pudo encontrar información del centro seleccionado.")
    else:
        st.info("Haz clic en un centro del mapa para ver su información.")
