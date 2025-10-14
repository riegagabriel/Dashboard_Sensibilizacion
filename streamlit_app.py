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
data = {
    "Categoría": ["A", "B", "C", "D", "E"],
    "Valor": [120, 80, 150, 90, 110],
    "Crecimiento": [5, -2, 7, 1, 3]
}
df = pd.DataFrame(data)

# -----------------------------------
# TÍTULO
# -----------------------------------
st.title("📊 Dashboard de Indicadores - Template")

# -----------------------------------
# INDICADORES ARRIBA
# -----------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total de registros", value=df["Valor"].sum())

with col2:
    st.metric(label="Promedio de Valor", value=round(df["Valor"].mean(), 2))

with col3:
    st.metric(label="Crecimiento promedio", value=str(round(df["Crecimiento"].mean(), 2)) + "%")

# -----------------------------------
# GRÁFICOS
# -----------------------------------
st.markdown("---")
st.subheader("📈 Gráfico interactivo")

fig = px.bar(df, x="Categoría", y="Valor", title="Valores por Categoría", text="Valor")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# TABLA
# -----------------------------------
st.subheader("📋 Datos fuente")
st.dataframe(df, use_container_width=True)

