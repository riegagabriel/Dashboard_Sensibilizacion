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
# GRÁFICO DE AVANCE POR DISTRITO (PLOTLY STACKED)
# ============================
import plotly.graph_objects as go

if resumen_distrital_copy is not None:
    st.markdown("## 📊 Avance de sensibilización por distrito")
    st.markdown("Selecciona una región para filtrar los resultados:")

    # ---------------------------
    # Preparación de datos
    # ---------------------------
    resumen_distrital_copy['pendientes'] = (
        resumen_distrital_copy['PROYECCION_ASIGNADOS']
        - resumen_distrital_copy['total_domicilios_sensibilizados']
    ).clip(lower=0)

    # ---------------------------
    # Filtro de región
    # ---------------------------
    regiones = ["Todos", "LIMA Y CALLAO", "Otras regiones"] + sorted(resumen_distrital_copy["region"].unique().tolist())
    seleccion_region = st.selectbox("Filtrar por región:", regiones)

    if seleccion_region == "Todos":
        df_filtrado = resumen_distrital_copy
    elif seleccion_region == "LIMA Y CALLAO":
        df_filtrado = resumen_distrital_copy[resumen_distrital_copy['region'].isin(['LIMA', 'CALLAO'])]
    elif seleccion_region == "Otras regiones":
        df_filtrado = resumen_distrital_copy[~resumen_distrital_copy['region'].isin(['LIMA', 'CALLAO'])]
    else:
        df_filtrado = resumen_distrital_copy[resumen_distrital_copy['region'] == seleccion_region]

    # Ordenar de mayor a menor avance
    df_filtrado = df_filtrado.sort_values(by="total_domicilios_sensibilizados", ascending=False)

    # ---------------------------
    # Gráfico Plotly
    # ---------------------------
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_filtrado['distrito_region'],
        x=df_filtrado['total_domicilios_sensibilizados'],
        name='Sensibilizados',
        orientation='h',
        marker=dict(color='#2ecc71'),
        text=df_filtrado['total_domicilios_sensibilizados'],
        textposition='outside'
    ))

    fig.add_trace(go.Bar(
        y=df_filtrado['distrito_region'],
        x=df_filtrado['pendientes'],
        name='Asignados',
        orientation='h',
        marker=dict(color='#e74c3c'),
        text=df_filtrado['pendientes'],
        textposition='outside'
    ))

    fig.update_layout(
        barmode='stack',
        height=700,
        title="Avance por distrito (Sensibilizados + Asignados)",
        xaxis_title="Número de domicilios",
        yaxis_title="",
        legend_title="Estado",
        margin=dict(l=10, r=10, t=50, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================
# NUEVA PESTAÑA: PODIO
# ============================

# Cargar archivo podio.xlsx
@st.cache_data
def cargar_podio():
    try:
        return pd.read_excel("podio.xlsx")
    except:
        st.error("⚠️ No se encontró archivo podio.xlsx. Súbelo a la carpeta del proyecto.")
        return None

podio_df = cargar_podio()

if podio_df is not None:
    # Crear pestañas
    tab1, tab2 = st.tabs(["Dashboard", "PODIO"])

    with tab2:
        st.markdown("## 🏆 Podio de Sensibilizadores")

        # ---------------------------
        # Gráfico interactivo Plotly
        # ---------------------------
        import plotly.graph_objects as go

        fig_podio = go.Figure()

        fig_podio.add_trace(go.Bar(
            y=podio_df['Sensibilizador'],
            x=podio_df['REGISTROS'],
            name='REGISTROS',
            orientation='h',
            marker=dict(color='#3498db'),
            text=podio_df['REGISTROS'],
            textposition='outside'
        ))

        fig_podio.add_trace(go.Bar(
            y=podio_df['Sensibilizador'],
            x=podio_df['Domicilios_sensibilizados'],
            name='Domicilios sensibilizados',
            orientation='h',
            marker=dict(color='#2ecc71'),
            text=podio_df['Domicilios_sensibilizados'],
            textposition='outside'
        ))

        fig_podio.update_layout(
            barmode='group',
            height=800,
            title="Registros y domicilios sensibilizados por Sensibilizador",
            xaxis_title="Cantidad",
            yaxis_title="Sensibilizador",
            margin=dict(l=10, r=10, t=50, b=10),
            legend_title="Indicador"
        )

        st.plotly_chart(fig_podio, use_container_width=True)

        # ---------------------------
        # Mostrar DataFrame
        # ---------------------------
        st.markdown("### 📋 Detalle del Podio")
        st.dataframe(podio_df)



