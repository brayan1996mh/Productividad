import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

# Configuración de la página
st.set_page_config(page_title="Productividad Emergencias ⚡", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# --- 1. BASE DE DATOS INTEGRADA ---
LISTA_CAPATACES = [
    "A. Aldonate", "A. Atoche", "A. Godoy", "A. Isuiza", "A. Torres", "A. Vigoria", 
    "A. Villanueva", "C. Hernandez", "C. Mayaudon", "C. Ñaupas", "C. Padilla", 
    "C. Salcedo", "D. Delgado", "D. Taquiri", "E. Ancco", "E. Antay", "E. Chihuan", 
    "E. Diaz", "E. Flores", "E. La rosa", "F. Lozano", "F. Ramos", "H. Cabrera", 
    "J. Abanto", "J. Apaza", "J. Arotinco", "J. Delgado", "J. Huari", "J. Panaifo", 
    "J. Parra", "J. Salvador", "J. Suarez", "J. Villanueva", "L. Angeles", "L. Ayala", 
    "L. Fiore", "M. Barrantes", "N. Pauro", "O. Aguilar", "P. Capcha", "R. Albites", 
    "R. Rojas", "R. Torres", "S. Jacinto", "S. Lazaro", "V. Bordon", "V. Campos", 
    "V. Orrillo", "V. Pérez", "V. Torres", "Y. Padilla"
]

DATOS_ACTIVIDADES = {
    "AP (Alumbrado Público)": [
        {"ACTIVIDAD": "Cable en cortocircuito de AP", "PESO": 0.61},
        {"ACTIVIDAD": "Cable a tierra AP", "PESO": 0.23},
        {"ACTIVIDAD": "Cable seccionado de AP", "PESO": 0.59},
        {"ACTIVIDAD": "Cable de AP dañado por terceros", "PESO": 0.46},
        {"ACTIVIDAD": "Cambio de fotocélula", "PESO": 0.46},
        {"ACTIVIDAD": "Retiro de luminaria", "PESO": 0.31},
        {"ACTIVIDAD": "Cambio de Llave AP", "PESO": 0.30},
        {"ACTIVIDAD": "Red Aérea en cortocircuito", "PESO": 0.27}
    ],
    "SP (Servicio Particular)": [
        {"ACTIVIDAD": "Cable en cortocircuito de SP", "PESO": 0.61},
        {"ACTIVIDAD": "Cable a Tierra/ Electrizado SP", "PESO": 0.51},
        {"ACTIVIDAD": "Cable seccionado De SP", "PESO": 0.59},
        {"ACTIVIDAD": "Cable de SP Dañado por terceros", "PESO": 0.46},
        {"ACTIVIDAD": "Red Aérea de AP y SP Sustraída", "PESO": 0.27}
    ],
    "POSTES": [
        {"ACTIVIDAD": "Cambio de poste chocado (con redes)", "PESO": 0.77},
        {"ACTIVIDAD": "Cambio de poste Corroído con redes", "PESO": 0.77},
        {"ACTIVIDAD": "Reposición de poste chocado sin redes", "PESO": 0.77},
        {"ACTIVIDAD": "Retiro de poste chocado", "PESO": 0.31}
    ],
    "CNX (Conexiones)": [
        {"ACTIVIDAD": "Conexión Subterránea quemada de AP", "PESO": 0.36},
        {"ACTIVIDAD": "Conexión Subterránea quemada de SP", "PESO": 0.36}
    ]
}

# --- 2. ESTILO VISUAL ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    input:disabled { color: #00E676 !important; font-weight: bold; background-color: rgba(0, 230, 118, 0.05) !important; }
    .stNumberInput div[data-baseweb="input"] input { color: #29B6F6 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Control de Productividad Emergencias")
st.markdown("---")

# --- 3. SELECCIÓN DE DATOS ---
st.subheader("Datos Generales")
c1, c2 = st.columns(2)
fecha = c1.date_input("FECHA", value=date.today())

# CAMPO SST LIMPIO
sst_input = c2.text_input("SST")

# LÓGICA: Se activa solo si son exactamente 7 caracteres y todos son números
sst_valida = sst_input.isnumeric() and len(sst_input) == 7

c3, c4 = st.columns(2)
capataz = c3.selectbox("CAPATAZ", ["Seleccione..."] + LISTA_CAPATACES)
circuito = c4.selectbox("CIRCUITO / SECTOR", ["Seleccione..."] + list(DATOS_ACTIVIDADES.keys()))

st.markdown("---")

if sst_valida and circuito != "Seleccione...":
    st.subheader(f"Actividades: {circuito}")
    opciones_act = [a["ACTIVIDAD"] for a in DATOS_ACTIVIDADES[circuito]]
    seleccion = st.multiselect("Agregar trabajos:", opciones_act, label_visibility="collapsed")

    if seleccion:
        st.markdown("---")
        st.subheader("Matriz de Avance")
        
        datos_finales = []
        for nombre_act in seleccion:
            peso_base = next(item["PESO"] for item in DATOS_ACTIVIDADES[circuito] if item["ACTIVIDAD"] == nombre_act)
            
            with st.container():
                st.write(f"### 🔧 {nombre_act}")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    estado = st.selectbox("Estado", ["Finalizado", "Devuelto", "Pendiente"], key=f"est_{nombre_act}")
                with col2:
                    st.text_input("Peso Base", value=f"{peso_base}%", disabled=True, key=f"pb_{nombre_act}")
                with col3:
                    avance = st.number_input("Avance (%)", 0, 100, 100, 10, key=f"av_{nombre_act}", format="%d%%")
                with col4:
                    peso_real = (avance / 100) * peso_base
                    st.text_input("Peso Real", value=f"{peso_real:.2f}%", disabled=True, key=f"pr_{nombre_act}")
                
                datos_finales.append({"Act": nombre_act, "Real": peso_real})
                st.markdown("---")

        # --- DASHBOARD ---
        total_p = sum(d["Real"] for d in datos_finales)
        col_gauge, col_info = st.columns([2, 1])
        
        with col_gauge:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_p,
                title = {'text': "Producción Total", 'font': {'color': "white"}},
                gauge = {
                    'axis': {'range': [0, 120], 'tickcolor': "white"},
                    'bar': {'color': "#00E676" if total_p >= 100 else "#FFEB3B"},
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col_info:
            st.metric("Puntaje Total", f"{total_p:.2f}%")
            if total_p >= 100:
                st.success("✅ Objetivo Cumplido")
            else:
                st.info(f"Falta {(100-total_p):.2f}%")

elif sst_input and not sst_valida:
    st.warning("⚠️ La SST debe contener exactamente 7 números para continuar.")
else:
    st.info("💡 Complete la SST (7 números) y el circuito para habilitar el registro.")
