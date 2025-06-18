import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import requests
from folium.plugins import MarkerCluster
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configurar página ---

st.set_page_config(
    page_title="Valencia Aprendes - Centros Educativos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS personalizado para menú con emojis ---

st.markdown("""
<style>
    /* Estilo menú lateral */
    .sidebar .stSelectbox > div > div {
        font-size: 1.2rem;
        font-weight: 600;
        color: #003366;
        background-color: #e0f3ff;
        border-radius: 12px;
        padding: 10px 15px;
        border: 2px solid #89c4f4;
        margin-bottom: 1rem;
    }
    /* Texto menú */
    .sidebar .stMarkdown h1 {
        color: #003366;
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 0.75rem;
        text-align: center;
        user-select: none;
    }
    /* Iconos en select */
    .sidebar .stSelectbox label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #00509e;
        user-select: none;
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
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df.dropna(subset=['latitude', 'longitude'], inplace=True)
        return df
    except Exception as e:
        st.error(f"No se pudo cargar la información de los centros: {e}")
        return pd.DataFrame()
    
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

# --- Menú lateral con emojis y texto con estilo ---
st.sidebar.markdown("# Menú Principal")

page = st.sidebar.selectbox(
    "Selecciona la vista",
    ("Mapa de Centros", "Estadísticas")
)

if page == "Mapa de Centros":
    col1, col2, col3 = st.columns([0.15, 0.6, 0.25])

    with col1:
        st.subheader("Filtros")

        nombres_colegios = ['Todos'] + sorted(df['nombre'].dropna().unique())
        nombre = st.selectbox("Nombre del centro", nombres_colegios)

        df_filtrado = df.copy()
        if nombre != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['nombre'] == nombre]

        municipios = ['Todos'] + sorted(df_filtrado['municipio'].dropna().unique())
        regimenes = ['Todos'] + sorted(df_filtrado['regimen'].dropna().unique())

        municipio = st.selectbox("Municipio", municipios)
        regimen = st.selectbox("Tipo de centro", regimenes)

        if municipio != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio]
        if regimen != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['regimen'] == regimen]

    with col2:
        st.subheader("Centros escolares Valencia")

        if nombre != 'Todos' and not df_filtrado.empty:
            centro_seleccionado = df_filtrado.iloc[0]
            mapa = folium.Map(
                location=[centro_seleccionado['latitude'], centro_seleccionado['longitude']],
                zoom_start=15,
                control_scale=True
            )
        else:
            mapa = folium.Map(location=[39.47, -0.38], zoom_start=12, control_scale=True)

        cluster = MarkerCluster().add_to(mapa)

        for _, row in df_filtrado.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                icon=folium.Icon(color="blue", icon="graduation-cap", prefix="fa"),
                tooltip=row['nombre']
            ).add_to(cluster)

        mapa_data = st_folium(mapa, width=850, height=500)

    with col3:
        st.subheader("🏫 Información")

        centro_seleccionado = None
        if mapa_data and mapa_data.get("last_object_clicked"):
            lat = mapa_data["last_object_clicked"]["lat"]
            lon = mapa_data["last_object_clicked"]["lng"]

            centro = df_filtrado[(df_filtrado["latitude"] == lat) & (df_filtrado["longitude"] == lon)]

            if not centro.empty:
                centro_seleccionado = centro.iloc[0]
                st.markdown(f"""
                    <div style="background:#ffffffdd; padding:15px; border-radius:15px; box-shadow: 0 4px 10px rgba(0,80,150,0.15); color:#004080; font-size:1rem;">
                        <p><strong>Nombre:</strong> {centro_seleccionado['nombre']}</p>
                        <p><strong>Dirección:</strong> {centro_seleccionado['direccion']}</p>
                        <p><strong>Municipio:</strong> {centro_seleccionado['municipio']}</p>
                        <p><strong>Provincia:</strong> {centro_seleccionado['provincia']}</p>
                        <p><strong>CP:</strong> {centro_seleccionado['CP']}</p>
                        <p><strong>Régimen:</strong> {centro_seleccionado['regimen']}</p>
                        <p><strong>Teléfono:</strong> {centro_seleccionado['telef']}</p>
                        <p><strong>Email:</strong> {centro_seleccionado['mail']}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("No se pudo encontrar información del centro seleccionado.")
        else:
            st.info("Haz clic en un marcador del mapa para ver la información del centro.")

elif page == "Estadísticas":
    st.title("Estadísticas de los centros educativos")

    # Gráfico 1: Distribución por régimen
    st.markdown("Centros por tipo de régimen")
    st.markdown("""
    Esta gráfica muestra la distribución porcentual de los centros educativos según su régimen (público, privado, concertado, etc.).
    Permite visualizar qué tipo de centros predominan en la región.
    """)
    regimen_counts = df['regimen'].value_counts().reset_index()
    regimen_counts.columns = ['Régimen', 'Cantidad']
    fig1 = px.pie(regimen_counts, names='Régimen', values='Cantidad',
                    color_discrete_sequence=px.colors.sequential.Blues, hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Top 10 municipios con más centros
    st.markdown("Municipios con más centros (Top 10)")
    st.markdown("""
    Aquí se muestran los 10 municipios con mayor cantidad de centros educativos.
    Es útil para identificar las zonas con mayor concentración de escuelas.
    """)
    municipio_counts = df['municipio'].value_counts().head(10).reset_index()
    municipio_counts.columns = ['Municipio', 'Centros']
    fig2 = px.bar(municipio_counts, x='Municipio', y='Centros',
                    color='Centros', text='Centros', color_continuous_scale='Blues')
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)
    
    
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
