import streamlit as st
import pandas as pd

st.title("Centros Educativos en Valencia")

df = pd.read_csv("centros-educativos-en-valencia.csv", sep=";" )

df2 = df.drop(["Geo Shape", "fax", "despecific","dgenerica_"],axis=1)

df2.columns = ['geo_point', 'codcen', 'nombre', 'regimen', 'direccion', 'CP',
        'municipio', 'provincia', 'telef', 'mail']

df2[["latitud","longitud"]] = df2["geo_point"].str.split(",", expand=True).astype(float)

df3 = df2.drop("geo_point",axis=1)


# Renombro para st.map
df3 = df3.rename(columns={"latitud": "latitude", "longitud": "longitude"})

# Muestro mapa con los puntos
st.map(df3[['latitude', 'longitude']])