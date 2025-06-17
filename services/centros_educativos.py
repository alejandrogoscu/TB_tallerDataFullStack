import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import requests
from folium.plugins import MarkerCluster


# --- Configurar página ---
st.set_page_config(
    page_title="Valencia Aprendes - Centros Educativos",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- CSS personalizado ---
st.markdown("""
<style>
    /* Fondo general */
    body, .css-18e3th9 {
        background: linear-gradient(135deg, #e0f3ff, #f7fbff);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Título principal */
    .css-1v3fvcr h1 {
        color: #003366;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    /* Subtítulos */
    .stSubheader {
        color: #00509e;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    /* Selectbox styling */
    div[data-baseweb="select"] > div {
        background-color: #f0f8ff !important;
        border-radius: 10px !important;
        border: 1px solid #89c4f4 !important;
        
        color: #003366 !important;
        font-weight: 600;
    }

    /* Tarjeta info centro */
    .info-card {
        background-color: #ffffffdd;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 80, 150, 0.15);
        margin-top: 15px;
        font-size: 1rem;
        color: #004080;
        line-height: 1.5;
    }
    .info-card strong {
        color: #00264d;
    }

    /* Mensajes info y warnings */
    .stAlert > div {
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
    }

  
</style>
""", unsafe_allow_html=True)

# --- Función para cargar datos desde la API ---
@st.cache_data
def cargar_centros():
    url = "https://tb-tallerdatafullstack.onrender.com/colegios"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        # Asegurar columnas lat y lon son float
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df.dropna(subset=['latitude', 'longitude'], inplace=True)
        return df
    except Exception as e:
        st.error(f"No se pudo cargar la información de los centros: {e}")
        return pd.DataFrame()

# --- Cargar datos ---
df = cargar_centros()

# --- Layout ---
col1, col2, col3 = st.columns([0.15, 0.6, 0.25])

# --- Columna 1: Filtros ---
with col1:
    st.subheader("Filtros")

    # Dropdown nombre colegio
    nombres_colegios = ['Todos'] + sorted(df['nombre'].dropna().unique())
    nombre = st.selectbox("Nombre del centro", nombres_colegios)

    # Filtrar por nombre si elegido
    df_filtrado = df.copy()
    if nombre != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['nombre'] == nombre]

    # Dropdown municipio y régimen basados en df_filtrado
    municipios = ['Todos'] + sorted(df_filtrado['municipio'].dropna().unique())
    regimenes = ['Todos'] + sorted(df_filtrado['regimen'].dropna().unique())

    municipio = st.selectbox("Municipio", municipios)
    regimen = st.selectbox("Tipo de centro", regimenes)

    # Aplicar filtros restantes
    if municipio != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio]
    if regimen != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['regimen'] == regimen]

# --- Columna 2: Mapa ---

with col2:
    st.subheader("Mapa de centros")

    # Si se ha seleccionado un colegio, hacer zoom a él
    if nombre != 'Todos' and not df_filtrado.empty:
        centro_seleccionado = df_filtrado.iloc[0]
        mapa = folium.Map(
            location=[centro_seleccionado['latitude'], centro_seleccionado['longitude']],
            zoom_start=15,
            control_scale=True
        )
    else:
        # Zoom por defecto en Valencia
        mapa = folium.Map(location=[39.47, -0.38], zoom_start=12, control_scale=True)

    # Crear agrupación de marcadores
    cluster = MarkerCluster().add_to(mapa)

    # Añadir marcadores al cluster
    for _, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            icon=folium.Icon(color="blue", icon="graduation-cap", prefix="fa"),
            tooltip=row['nombre']
        ).add_to(cluster)

    mapa_data = st_folium(mapa, width=850, height=500)

# --- Columna 3: Detalles del centro ---
with col3:
    st.subheader("Información")

    if mapa_data and mapa_data.get("last_object_clicked"):
        lat = mapa_data["last_object_clicked"]["lat"]
        lon = mapa_data["last_object_clicked"]["lng"]

        centro = df_filtrado[(df_filtrado["latitude"] == lat) & (df_filtrado["longitude"] == lon)]

        if not centro.empty:
            c = centro.iloc[0]
            st.markdown(f"""
                <div class="info-card">
                    <p><strong>Nombre:</strong> {c['nombre']}</p>
                    <p><strong>Dirección:</strong> {c['direccion']}</p>
                    <p><strong>Municipio:</strong> {c['municipio']}</p>
                    <p><strong>Provincia:</strong> {c['provincia']}</p>
                    <p><strong>CP:</strong> {c['CP']}</p>
                    <p><strong>Régimen:</strong> {c['regimen']}</p>
                    <p><strong>Teléfono:</strong> {c['telef']}</p>
                    <p><strong>Email:</strong> {c['mail']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No se pudo encontrar información del centro seleccionado.")
    else:
        st.info("Haz clic en un marcador del mapa para ver la información del centro.")
