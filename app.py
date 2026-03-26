import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import re

# --- CONFIGURACIÓN ---
st.set_page_config(
    page_title="⚡ Productividad Emergencias",
    page_icon="⚡",
    layout="wide"
)

# --- DATA ---
LISTA_CAPATACES = [
    "A. Aldonate","A. Atoche","A. Godoy","A. Isuiza","A. Torres","A. Vigoria",
    "A. Villanueva","C. Hernandez","C. Mayaudon","C. Ñaupas","C. Padilla",
    "C. Salcedo","D. Delgado","D. Taquiri","E. Ancco","E. Antay","E. Chihuan",
    "E. Diaz","E. Flores","E. La rosa","F. Lozano","F. Ramos","H. Cabrera",
    "J. Abanto","J. Apaza","J. Arotinco","J. Delgado","J. Huari","J. Panaifo",
    "J. Parra","J. Salvador","J. Suarez","J. Villanueva","L. Angeles","L. Ayala",
    "L. Fiore","M. Barrantes","N. Pauro","O. Aguilar","P. Capcha","R. Albites",
    "R. Rojas","R. Torres","S. Jacinto","S. Lazaro","V. Bordon","V. Campos",
    "V. Orrillo","V. Pérez","V. Torres","Y. Padilla"
]

DATOS_ACTIVIDADES = {
    "AP": [
        {"ACTIVIDAD": "Cable en cortocircuito de AP", "PESO": 0.62},
        {"ACTIVIDAD": "Cable a tierra AP", "PESO": 0.23},
        {"ACTIVIDAD": "Cambio de fotocélula", "PESO": 0.46},
        {"ACTIVIDAD": "Retiro de luminaria", "PESO": 0.31},
    ],
    "SP": [
        {"ACTIVIDAD": "Cable en cortocircuito de SP", "PESO": 0.62},
        {"ACTIVIDAD": "Cable a Tierra SP", "PESO": 0.52},
        {"ACTIVIDAD": "Cambio de tablero", "PESO": 0.42},
    ]
}

# --- ESTILO ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg,#0b1c2c,#050a0f);
}
.estado-ok {color:#00E676;font-weight:bold;}
.estado-mal {color:#FF5252;font-weight:bold;}
.estado-mid {color:#FFD54F;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("⚡ Control de Productividad")

# --- INPUTS ---
col1, col2 = st.columns(2)
fecha = col1.date_input("Fecha", value=date.today())
sst = col2.text_input("SST")

valida_sst = bool(re.match(r'^\d{7}$', sst)) if sst else False

col3, col4 = st.columns(2)
capataz = col3.selectbox("Capataz", ["Seleccione"] + LISTA_CAPATACES)
circuito = col4.selectbox("Circuito", ["Seleccione"] + list(DATOS_ACTIVIDADES.keys()))

st.divider()

# --- VALIDACIÓN ---
if not valida_sst and sst:
    st.warning("⚠️ SST inválida (7 dígitos)")
elif valida_sst and circuito != "Seleccione":

    actividades = DATOS_ACTIVIDADES[circuito]
    nombres = [a["ACTIVIDAD"] for a in actividades]

    seleccion = st.multiselect("Actividades", nombres)

    if seleccion:
        st.subheader("📊 Matriz de Avance")

        resultados = []

        for act in seleccion:
            peso = next(a["PESO"] for a in actividades if a["ACTIVIDAD"] == act)

            col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])

            with col1:
                st.write(f"🔧 {act}")

            with col2:
                estado = st.selectbox("Estado", ["Finalizado","Devuelto","Pendiente"], key=act)

            with col3:
                st.write(f"{peso*100:.0f}%")

            with col4:
                avance = st.number_input(
                    "Avance",
                    min_value=0,
                    max_value=100,
                    value=100,
                    step=10,
                    key=f"av_{act}"
                )

            peso_real = (avance/100) * peso

            with col5:
                st.write(f"{peso_real*100:.2f}%")

            # COLOR SEGÚN ESTADO
            if estado == "Finalizado":
                st.markdown('<span class="estado-ok">✔ Finalizado</span>', unsafe_allow_html=True)
            elif estado == "Devuelto":
                st.markdown('<span class="estado-mal">✖ Devuelto</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="estado-mid">⏳ Pendiente</span>', unsafe_allow_html=True)

            resultados.append({
                "Actividad": act,
                "Base": peso*100,
                "Real": peso_real*100
            })

            st.divider()

        # --- MÉTRICAS ---
        df = pd.DataFrame(resultados)
        total = df["Real"].sum()

        colA, colB, colC = st.columns(3)

        colA.metric("Producción Total", f"{total:.2f}%")

        if total >= 100:
            colB.success("✅ Cumplido")
        elif total >= 70:
            colB.warning("⚠️ En progreso")
        else:
            colB.error("❌ Bajo")

        colC.metric("Actividades", len(df))

        # --- ALERTA INTELIGENTE ---
        if total < 50:
            st.error("🚨 Riesgo crítico de incumplimiento")
        elif total < 80:
            st.warning("⚠️ Riesgo moderado")

        # --- GAUGE ---
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total,
            title={'text': "Avance Total"},
            gauge={
                'axis': {'range': [0, 120]},
                'bar': {'color': "green" if total>=100 else "orange"},
                'threshold': {'value':100}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # --- BARRAS ---
        fig2 = go.Figure([
            go.Bar(name="Base", x=df["Actividad"], y=df["Base"]),
            go.Bar(name="Real", x=df["Actividad"], y=df["Real"])
        ])

        fig2.update_layout(barmode="group")
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("👉 Ingresa SST válida y selecciona circuito")
