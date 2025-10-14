import streamlit as st
import pandas as pd

# ---------------------------
# CONFIGURACIÓN
# ---------------------------
st.set_page_config(page_title="Dashboard Sensibilización", layout="wide")
st.title("📊 Campaña de Sensibilización")

# ---------------------------
# CARGA DE DATOS
# ---------------------------
@st.cache_data
def cargar_datos():
    try:
        # Primero intenta cargar Excel
        return pd.read_excel("value_box_sens.xlsx")
    except:
        try:
            # Si no hay Excel intenta cargar CSV
            return pd.read_csv("value_box_sens.csv")
        except:
            st.error("⚠️ No se encontró archivo de datos. Sube un .xlsx o .csv.")
            return None

df = cargar_datos()

if df is not None:
    # ---------------------------
    # VALUE BOXES
    # ---------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🏡 Domicilios alcanzados", int(df.loc[df["Variable"] == "dom_alcanzados", "Valor"].values[0]))
    with col2:
        st.metric("📣 Domicilios sensibilizados", int(df.loc[df["Variable"] == "dom_sensibilizados", "Valor"].values[0]))
    with col3:
        st.metric("👶 Caras de niño sensibilizadas", int(df.loc[df["Variable"] == "cara_nino_sens", "Valor"].values[0]))
    with col4:
        st.metric("👥 Total personas sensibilizadas", int(df.loc[df["Variable"] == "total_personas_sen", "Valor"].values[0]))

import plotly.graph_objects as go

# Obtener valor real desde tu DataFrame
logrado = int(df.loc[df["Variable"] == "dom_sensibilizados", "Valor"].values[0])
meta = 13343
avance = (logrado / meta) * 100  # porcentaje

st.markdown("### 🎯 Avance hacia la meta de domicilios sensibilizados")

# Crear gráfico Gauge
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=avance,
    number={'suffix': "%"},
    delta={'reference': 100, 'increasing': {'color': "green"}},
    gauge={
        'axis': {'range': [0, max(120, avance)], 'tickwidth': 1},
        'bar': {'color': "green"},
        'steps': [
            {'range': [0, 50], 'color': "#FFE5CC"},
            {'range': [50, 100], 'color': "#FFD27F"},
            {'range': [100, max(120, avance)], 'color': "#B6FFB6"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 100
        }
    }
))

fig.update_layout(height=350, margin=dict(l=30, r=30, t=50, b=0))
st.plotly_chart(fig, use_container_width=True)

# Mensaje adicional
if avance > 100:
    st.success(f"✅ ¡Meta superada! {logrado:,} domicilios sensibilizados ({avance:.1f}% del objetivo)")
else:
    st.info(f"Avance actual: {avance:.1f}% ({logrado:,} de {meta:,})")
