import streamlit as st
import pandas as pd
import numpy as np
import pickle

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(
    page_title="Predicción de Precio de Casas",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Predictor de Precio Medio de Casas")
st.write("Modifica las variables y obtén una predicción del precio estimado.")

# =============================
# CARGAR MODELO
# =============================
@st.cache_resource
def cargar_modelo():
    with open("modelo_casas.pkl", "rb") as f:
        modelo = pickle.load(f)
    return modelo

modelo = cargar_modelo()

# =============================
# SIDEBAR - INPUTS
# =============================
st.sidebar.header("Variables de Entrada")

longitud = st.sidebar.slider("Longitud", -125.0, -113.0, -122.0)
latitud = st.sidebar.slider("Latitud", 32.0, 42.0, 37.0)

edad_mediana_vivienda = st.sidebar.slider(
    "Edad mediana vivienda", 1, 52, 25
)

total_habitaciones = st.sidebar.number_input(
    "Total habitaciones", min_value=1, value=2000
)

total_dormitorios = st.sidebar.number_input(
    "Total dormitorios", min_value=1, value=400
)

poblacion = st.sidebar.number_input(
    "Población", min_value=1, value=1000
)

hogares = st.sidebar.number_input(
    "Hogares", min_value=1, value=350
)

ingreso_mediano = st.sidebar.slider(
    "Ingreso mediano", 0.0, 15.0, 4.0
)

proximidad_oceano = st.sidebar.selectbox(
    "Proximidad al océano",
    ["<1H OCEAN", "INLAND", "NEAR OCEAN", "NEAR BAY", "ISLAND"]
)

# =============================
# PREPARAR INPUT
# =============================
input_data = pd.DataFrame([{
    "longitud": longitud,
    "latitud": latitud,
    "edad_mediana_vivienda": edad_mediana_vivienda,
    "total_habitaciones": total_habitaciones,
    "total_dormitorios": total_dormitorios,
    "poblacion": poblacion,
    "hogares": hogares,
    "ingreso_mediano": ingreso_mediano,
    "proximidad_oceano": proximidad_oceano
}])

# =============================
# PREDICCIÓN
# =============================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Valores Seleccionados")
    st.dataframe(input_data)

with col2:
    st.subheader("Predicción")

    if st.button("Predecir Precio"):
        try:
            prediccion = modelo.predict(input_data)[0]

            st.success(f"Precio estimado: ${prediccion:,.2f}")

            st.metric(
                label="Valor estimado",
                value=f"${prediccion:,.0f}"
            )

        except Exception as e:
            st.error(f"Error en predicción: {e}")

# =============================
# GRÁFICAS
# =============================
st.markdown("---")
st.subheader("📊 Visualización de Variables")

col3, col4 = st.columns(2)

with col3:
    st.write("Habitaciones vs Dormitorios")

    df_hab = pd.DataFrame(
        {
            "Cantidad": [
                total_habitaciones,
                total_dormitorios
            ]
        },
        index=["Habitaciones", "Dormitorios"]
    )

    st.bar_chart(df_hab)

with col4:
    st.write("Población vs Hogares")

    df_pob = pd.DataFrame(
        {
            "Cantidad": [
                poblacion,
                hogares
            ]
        },
        index=["Población", "Hogares"]
    )

    st.bar_chart(df_pob)

st.write("Resumen general de variables")

df_resumen = pd.DataFrame(
    {
        "Valor": [
            edad_mediana_vivienda,
            ingreso_mediano,
            total_habitaciones / 100,
            poblacion / 100
        ]
    },
    index=[
        "Edad vivienda",
        "Ingreso",
        "Habitaciones (/100)",
        "Población (/100)"
    ]
)

st.line_chart(df_resumen)
