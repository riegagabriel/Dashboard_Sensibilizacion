import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------
st.set_page_config(page_title="Dashboard Demo", layout="wide")

# -----------------------------------
# DATA DE PRUEBA (PUEDES CAMBIARLA)
# -----------------------------------
df = pd.read_excel("value_box_sens.xlsx")
# -----------------------------------
# SENSIBILIZACIÓN
# -----------------------------------
st.title("📊Indicadores - Campaña de Sensibilización(27/06 - 14/10")

# -----------------------------------
# VALUE BOXES (INDICADORES ARRIBA)
# -----------------------------------
st.subheader("📌 Indicadores principales")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="🏡 Domicilios alcanzados", value=indicadores.loc[0, "Valor"])

with col2:
    st.metric(label="📣 Domicilios sensibilizados", value=indicadores.loc[1, "Valor"])

with col3:
    st.metric(label="👶 Caras de niño sensibilizadas", value=indicadores.loc[2, "Valor"])

with col4:
    st.metric(label="👥 Total personas sensibilizadas", value=indicadores.loc[3, "Valor"])

