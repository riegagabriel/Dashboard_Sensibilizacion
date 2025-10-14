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

# --- Datos del progreso ---
# Obtener valor de domicilios sensibilizados desde el DataFrame
logrado = int(df.loc[df["Variable"] == "dom_sensibilizados", "Valor"].values[0])
meta = 13343
avance = logrado / meta

st.markdown("### 🎯 Avance hacia la meta de domicilios sensibilizados")

# Mostrar barra de progreso
if avance <= 1:
    st.progress(avance)
else:
    st.progress(1.0)  # Progreso completo si supera meta

# Mostrar texto explicativo
if avance > 1:
    st.success(f"✅ Meta superada: {logrado:,} domicilios sensibilizados ({avance*100:.1f}% del objetivo)")
else:
    st.info(f"Progreso actual: {avance*100:.1f}% ({logrado:,} de {meta:,} domicilios)")

