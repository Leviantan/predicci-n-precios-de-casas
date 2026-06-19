import streamlit as st
import pandas as pd
import requests

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Predicción valor vivienda",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Predicción del valor medio de vivienda")
st.write("Modifica las variables y consulta el modelo desplegado en DataRobot.")

# =========================
# SECRETS DATAROBOT
# =========================
DATAROBOT_API_KEY = st.secrets["DATAROBOT_API_KEY"]
DATAROBOT_DEPLOYMENT_ID = st.secrets["DATAROBOT_DEPLOYMENT_ID"]
DATAROBOT_HOST = st.secrets["DATAROBOT_HOST"]

PREDICTION_URL = (
    f"{DATAROBOT_HOST}/predApi/v1.0/deployments/"
    f"{DATAROBOT_DEPLOYMENT_ID}/predictions"
)

HEADERS = {
    "Authorization": f"Bearer {DATAROBOT_API_KEY}",
    "Content-Type": "text/plain; charset=UTF-8"
}

# =========================
# FORMULARIO
# =========================
st.subheader("Variables de entrada")

longitud = st.number_input("Longitud", value=-122.23, step=0.01)
latitud = st.number_input("Latitud", value=37.88, step=0.01)

edad_mediana_vivienda = st.slider(
    "Edad mediana de la vivienda",
    1, 60, 30
)

total_habitaciones = st.number_input(
    "Total habitaciones",
    min_value=1,
    value=880
)

total_dormitorios = st.number_input(
    "Total dormitorios",
    min_value=1,
    value=129
)

poblacion = st.number_input(
    "Población",
    min_value=1,
    value=322
)

hogares = st.number_input(
    "Hogares",
    min_value=1,
    value=126
)

ingreso_mediano = st.number_input(
    "Ingreso mediano",
    min_value=0.0,
    value=8.3252,
    step=0.01
)

proximidad_oceano = st.selectbox(
    "Proximidad al océano",
    ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]
)

# =========================
# DATOS
# =========================
datos = pd.DataFrame([{
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

st.subheader("Datos enviados al modelo")
st.dataframe(datos)

csv_data = datos.to_csv(index=False)

# =========================
# GRÁFICAS
# =========================
st.subheader("📊 Visualización")

col1, col2 = st.columns(2)

with col1:
    df_hab = pd.DataFrame(
        {"Cantidad": [total_habitaciones, total_dormitorios]},
        index=["Habitaciones", "Dormitorios"]
    )
    st.bar_chart(df_hab)

with col2:
    df_pob = pd.DataFrame(
        {"Cantidad": [poblacion, hogares]},
        index=["Población", "Hogares"]
    )
    st.bar_chart(df_pob)

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
        "Edad",
        "Ingreso",
        "Habitaciones/100",
        "Población/100"
    ]
)

st.line_chart(df_resumen)

# =========================
# PREDICCIÓN
# =========================
if st.button("Predecir valor de vivienda"):
    try:
        response = requests.post(
            PREDICTION_URL,
            headers=HEADERS,
            data=csv_data.encode("utf-8")
        )

        if response.status_code == 200:
            resultado = response.json()
            prediccion = resultado["data"][0]["prediction"]

            st.success("Predicción realizada correctamente")
            st.metric(
                "Valor medio estimado",
                f"${prediccion:,.2f}"
            )

            with st.expander("Respuesta completa"):
                st.json(resultado)

        else:
            st.error(f"Error API: {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
