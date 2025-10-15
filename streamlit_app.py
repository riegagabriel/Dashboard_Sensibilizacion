import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
        return pd.read_excel("value_box_sens.xlsx")
    except:
        try:
            return pd.read_csv("value_box_sens.csv")
        except:
            st.error("⚠️ No se encontró archivo de datos. Sube un .xlsx o .csv.")
            return None

df = cargar_datos()

# ---------------------------
# CARGA DE RESUMEN DISTRITAL
# ---------------------------
@st.cache_data
def cargar_resumen_distrital():
    try:
        return pd.read_excel("resumen_distrital_copy.xlsx")
    except:
        try:
            return pd.read_csv("resumen_distrital_copy.csv")
        except:
            st.error("⚠️ No se encontró archivo resumen_distrital copy (.xlsx o .csv). Súbelo a la carpeta del proyecto.")
            return None

resumen_distrital_copy = cargar_resumen_distrital()


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

    # ---------------------------
    # AVANCE HACIA META
    # ---------------------------
    logrado = int(df.loc[df["Variable"] == "dom_sensibilizados", "Valor"].values[0])
    meta = 13343
    avance = logrado / meta  # proporción alcanzada

    st.markdown("### 🎯 Avance hacia la meta de domicilios sensibilizados")

    # HTML para barra de progreso
    progress_html = f"""
    <div style="border:1px solid #ddd; padding:15px; border-radius:10px; background-color:#f9f9f9;">
      <p style="margin:0; font-weight:bold; font-size:16px;">
        Meta: {meta:,}
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
        st.success(f"🚀 ¡Meta superada por {(avance - 1) * 100:.1f}%!")
    else:
        st.info(f"📈 Progreso actual: {avance*100:.1f}% del objetivo.")

# ============================
# GRÁFICO DE AVANCE POR DISTRITO
# ============================
if resumen_distrital_copy is not None:

    st.markdown("## 📊 Avance de sensibilización por distrito")

    # Calcular pendientes
    resumen_distrital_copy['pendientes'] = resumen_distrital_copy['PROYECCION_ASIGNADOS'] - resumen_distrital_copy['total_domicilios_sensibilizados']
    resumen_distrital_copy['pendientes'] = resumen_distrital_copy['pendientes'].clip(lower=0)

    # Separar Lima y Callao vs otras regiones
    lima_callao = resumen_distrital_copy[resumen_distrital_copy['region'].isin(['LIMA', 'CALLAO'])].copy()
    otras_regiones = resumen_distrital_copy[~resumen_distrital_copy['region'].isin(['LIMA', 'CALLAO'])].copy()

    # Ordenar
    lima_callao = lima_callao.sort_values('total_domicilios_sensibilizados', ascending=True)
    otras_regiones = otras_regiones.sort_values('total_domicilios_sensibilizados', ascending=True)

    # Crear gráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 12))

    def crear_grafico(df, ax, titulo):
        distritos = df['distrito_region'].values
        sensibilizados = df['total_domicilios_sensibilizados'].values
        pendientes = df['pendientes'].values
        
        y_pos = np.arange(len(distritos))
        ax.barh(y_pos, sensibilizados, label='Sensibilizados', color='#2ecc71')
        ax.barh(y_pos, pendientes, left=sensibilizados, label='Pendientes', color='#e74c3c')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(distritos, fontsize=9)
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.set_xlabel('Domicilios')
        ax.legend()

    # Dibujar gráficos
    if not lima_callao.empty:
        crear_grafico(lima_callao, ax1, 'LIMA Y CALLAO')
    else:
        ax1.text(0.5, 0.5, 'Sin datos', ha='center')

    if not otras_regiones.empty:
        crear_grafico(otras_regiones, ax2, 'OTRAS REGIONES')
    else:
        ax2.text(0.5, 0.5, 'Sin datos', ha='center')

    st.pyplot(fig)



