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

import streamlit as st

# Obtener el avance desde tu DataFrame
logrado = int(df.loc[df["Variable"] == "dom_sensibilizados", "Valor"].values[0])
meta = 13343
avance = logrado / meta  # porcentaje decimal

# Bloque visual
st.markdown("### 🎯 Avance hacia la meta de domicilios sensibilizados")

# Contenedor estilizado
progress_html = f"""
<div style="border:1px solid #ddd; padding:15px; border-radius:10px; background-color:#f9f9f9;">
  <p style="margin:0; font-weight:bold; font-size:16px;">
    Meta: {meta:,}
    <span style="float:right;">{'│' if advance <= 1 else ''}</span>
  </p>
  <div style="margin-top:10px; background-color:#e6e6e6; border-radius:8px; height:28px;">
    <div style="
      width:{min(avance*100, 100)}%;
      background-color:#007BFF;
      height:100%;
      border-radius:8px;
    "></div>
  </div>
  <p style="margin-top:8px; font-size:16px; font-weight:bold;">
    Avance: {logrado:,} 
    <span style="color:green; font-weight:bold;">
      ✅ ({avance*100:.1f}% del objetivo)
    </span>
  </p>
</div>
"""

st.markdown(progress_html, unsafe_allow_html=True)

# Mensaje adicional
if avance > 1:
    st.success(f"🚀 ¡Meta superada por {((avance - 1) * 100):.1f}%! Excelente avance.")
else:
    st.info(f"Progreso actual: {avance*100:.1f}% del objetivo.")

# Mensaje adicional
if avance > 100:
    st.success(f"✅ ¡Meta superada! {logrado:,} domicilios sensibilizados ({avance:.1f}% del objetivo)")
else:
    st.info(f"Avance actual: {avance:.1f}% ({logrado:,} de {meta:,})")
