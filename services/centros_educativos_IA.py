import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configurar la página ---
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
# --- IA ---
@st.cache_data(show_spinner=False)

def preguntar_ia(prompt_texto):
    
    API_URL = "https://router.huggingface.co/together/v1/chat/completions"
    
    token = os.getenv("HUGGINGFACE_TOKEN")

    if not token:
        return "Token de Hugging Face no encontrado."

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt_texto
            }
        ],
        "model": "mistralai/Mistral-7B-Instruct-v0.3"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        result = response.json()

        # Extraer el mensaje de respuesta del modelo
        
        return result["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        return "La IA tardó demasiado en responder."
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con la IA: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

# --- Cargar datos ---
df = cargar_centros()

# --- Layout en 3 columnas ---
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

# --- Columna 1: Filtros ---
with col1:
    st.subheader("🔎 Filtros")

    # Asegurarse de que las columnas existen y manejar NaN
    municipios_disponibles = ['Todos'] + sorted(df['municipio'].dropna().unique().tolist())
    regimenes_disponibles = ['Todos'] + sorted(df['regimen'].dropna().unique().tolist())

    municipio_seleccionado = st.selectbox("Municipio", municipios_disponibles, key="municipio_filter")
    regimen_seleccionado = st.selectbox("Tipo de centro", regimenes_disponibles, key="regimen_filter")

# --- Filtrar dataframe ---
df_filtrado = df.copy()

if municipio_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio_seleccionado]
if regimen_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['regimen'] == regimen_seleccionado]

# --- Columna 2: Mapa ---
with col2:
    st.subheader("🗺️ Mapa de centros")

    if not df_filtrado.empty:
        center_lat = df_filtrado['latitude'].mean()
        center_lon = df_filtrado['longitude'].mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    else:
        m = folium.Map(location=[39.47, -0.38], zoom_start=12) # Centro de Valencia por defecto

    for _, row in df_filtrado.iterrows():
        if pd.notna(row["latitude"]) and pd.notna(row["longitude"]):
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=row["nombre"],
                tooltip=row["nombre"],
                icon=folium.Icon(color="blue", icon="graduation-cap", prefix="fa")
            ).add_to(m)

    mapa_data = st_folium(m, width=800, height=500, key="folium_map")

# --- Columna 3: Detalles del centro y respuesta de la IA ---
with col3:
    st.subheader("🏫 Información del centro")

    centro_seleccionado = None
    if mapa_data and mapa_data.get("last_object_clicked"):
        lat = mapa_data["last_object_clicked"]["lat"]
        lon = mapa_data["last_object_clicked"]["lng"]

        # Buscar el centro en el DataFrame original para obtener todos los detalles
        centro = df[(df["latitude"] == lat) & (df["longitude"] == lon)]

        if not centro.empty:
            centro_seleccionado = centro.iloc[0]
            st.markdown(f"**Nombre:** {centro_seleccionado['nombre']}")
            st.markdown(f"**Dirección:** {centro_seleccionado['direccion']}")
            st.markdown(f"**Municipio:** {centro_seleccionado['municipio']}")
            st.markdown(f"**Provincia:** {centro_seleccionado['provincia']}")
            st.markdown(f"**CP:** {centro_seleccionado['CP']}")
            st.markdown(f"**Régimen:** {centro_seleccionado['regimen']}")
            st.markdown(f"**Teléfono:** {centro_seleccionado['telef']}")
            st.markdown(f"**Email:** {centro_seleccionado['mail']}")

# --- Generar prompt inicial sobre el origen ---

st.markdown("---")  
st.subheader("🤖 Origen del centro según la IA:")

if centro_seleccionado is not None:
    prompt_origen = (
        f"¿Cuál es el posible origen histórico o institucional del centro educativo llamado {centro_seleccionado['nombre']}? "
        f"ubicado en '{centro_seleccionado['direccion']}', municipio de '{centro_seleccionado['municipio']}', "
        f"provincia de '{centro_seleccionado['provincia']}'. "
    )

    with st.spinner("Preguntando a la IA sobre el origen del centro..."):
        respuesta_origen = preguntar_ia(prompt_origen)
        st.info(respuesta_origen)
else:
    st.info("Selecciona un centro en el mapa para conocer sus orígenes y hacer preguntas.")


# --- Campo de pregunta personalizada ---

st.markdown("---")
st.subheader("📝 Haz otra pregunta sobre este centro")

if centro_seleccionado is not None:
    pregunta_usuario = st.text_input("Escribe tu pregunta sobre el centro", placeholder="¿Qué tipo de estudiantes asisten a este centro?")

    if pregunta_usuario:
        # Construir prompt con contexto + pregunta del usuario
        prompt_personalizado = (
            f"Tengo una pregunta sobre un centro educativo llamado '{centro_seleccionado['nombre']}', "
            f"La pregunta es: {pregunta_usuario}"
        )

        with st.spinner("Consultando la IA..."):
            respuesta_personalizada = preguntar_ia(prompt_personalizado)
            st.success(respuesta_personalizada)
else:
    st.info("Selecciona un centro para habilitar las preguntas personalizadas.")


