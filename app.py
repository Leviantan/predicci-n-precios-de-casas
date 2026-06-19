import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Intentar importar matplotlib sin romper la app
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_OK = True
except ModuleNotFoundError:
    MATPLOTLIB_OK = False

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
# CARGAR DATASET
# =============================
@st.cache_data
def cargar_data():
    try:
        df = pd.read_csv("housing.csv")
        return df
    except:
        return None

df = cargar_data()

# =============================
# SIDEBAR
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
# INPUT DATA
# =============================
input_data = pd.DataFrame({
    "longitud": [longitud],
    "latitud": [latitud],
    "edad_mediana_vivienda": [edad_mediana_vivienda],
    "total_habitaciones": [total_habitaciones],
    "total_dormitorios": [total_dormitorios],
    "poblacion": [poblacion],
    "hogares": [hogares],
    "ingreso_mediano": [ingreso_mediano],
    "proximidad_oceano": [proximidad_oceano]
})

# =============================
# PREDICCIÓN
# =============================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Valores Seleccionados")
    st.dataframe(input_data)

with col2:
    st.subheader("Predicción")

    if st.button("Predecir Precio"):
        try:
            prediccion = modelo.predict(input_data)[0]

            st.success(f"Precio estimado: ${prediccion:,.2f}")
            st.metric("Valor estimado", f"${prediccion:,.0f}")

        except Exception as e:
            st.error(f"Error al predecir: {e}")

# =============================
# GRÁFICAS
# =============================
st.markdown("---")
st.subheader("Visualización")

if not MATPLOTLIB_OK:
    st.warning("Matplotlib no está instalado. Instala la libría para ver gráficas.")

elif df is not None:
    col3, col4 = st.columns(2)

    with col3:
        if "median_income" in df.columns and "median_house_value" in df.columns:
            st.write("Ingreso vs Precio")
            fig, ax = plt.subplots()
            ax.scatter(
                df["median_income"],
                df["median_house_value"],
                alpha=0.3
            )
            ax.set_xlabel("Ingreso")
            ax.set_ylabel("Precio")
            st.pyplot(fig)

    with col4:
        if "median_house_value" in df.columns:
            st.write("Distribución de precios")
            fig2, ax2 = plt.subplots()
            ax2.hist(df["median_house_value"], bins=30)
            ax2.set_xlabel("Precio")
            ax2.set_ylabel("Frecuencia")
            st.pyplot(fig2)

else:
    st.info("No se encontró housing.csv.")
