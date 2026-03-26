import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import re

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

# --- 2. ESTILO VISUAL (FONDO OPERACIONAL) ---
styl = f"""
<style>
    .stApp {{
        background-image: linear-gradient(180deg, rgba(5, 15, 25, 0.85) 0%, rgba(5, 10, 15, 0.95) 100%), 
                          url('https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .stMarkdown, .stSubheader, .stTitle {{
        margin-top: -10px !important;
        margin-bottom: 2px !important;
        text-shadow: 1px 1px 3px black;
    }}
    
    input:disabled {{
        color: #00E676 !important;
        -webkit-text-fill-color: #00E676 !important;
        font-weight: bold;
        background-color: rgba(0, 230, 118, 0.1) !important;
        border: 1px solid #00E676;
    }}
    
    .stNumberInput div[data-baseweb="input"] input {{
        color: #29B6F6 !important;
        font-weight: bold;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

st.title("⚡ Control de Productividad Emergencias")
st.markdown("---")

# --- 3. SELECCIÓN DE DATOS ---
st.subheader("Datos Generales")
c1, c2 = st.columns(2)
fecha = c1.date_input("FECHA", value=date.today())
sst_input = c2.text_input("SST")

# Lógica de validación SST
sst_valida = False
if sst_input:
    if re.match(r'^\d{7}$', sst_input):
        sst_valida = True

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
        
        datos_para_tabla = []
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
                
                datos_para_tabla.append({
                    "Actividad": nombre_act, 
                    "Peso Base": peso_base, 
                    "Peso Real": peso_real
                })
                st.markdown("---")

        # --- 4. DASHBOARD ---
        if datos_para_tabla:
            total_p = sum(d["Peso Real"] for d in datos_para_tabla)
            
            col_gauge, col_info = st.columns([2, 1])
            
            with col_gauge:
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = total_p,
                    title = {'text': "Producción Total (%)", 'font': {'color': "white"}},
                    gauge = {
                        'axis': {'range': [0, 120], 'tickcolor': "white"},
                        'bar': {'color': "#00E676" if total_p >= 100 else "#FFEB3B"},
                        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}
                    }
                ))
                fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
                st.plotly_chart(fig_gauge, use_container_width=True)

            with col_info:
                st.metric("Puntaje Total", f"{total_p:.2f}%")
                if total_p >= 100:
                    st.success("✅ Objetivo Cumplido")
                else:
                    st.info(f"Falta {(100-total_p):.2f}%")

            # --- GRÁFICA DE BARRAS (MÉTODO INFALIBLE) ---
            st.write("### Comparativo de Pesos")
            
            # Extraemos las listas de datos manualmente para evitar errores de pandas
            x_actividades = [d["Actividad"] for d in datos_para_tabla]
            y_base = [d["Peso Base"] for d in datos_para_tabla]
            y_real = [d["Peso Real"] for d in datos_para_tabla]

            # Construimos la gráfica ladrillo por ladrillo
            fig_bar = go.Figure(data=[
                go.Bar(name='Peso Base', x=x_actividades, y=y_base, marker_color='#B0BEC5'),
                go.Bar(name='Peso Real', x=x_actividades, y=y_real, marker_color='#0288D1')
            ])
            
            # Aplicamos el diseño
            fig_bar.update_layout(
                barmode='group',
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45,
                xaxis_title="Actividad",
                yaxis_title="Porcentaje (%)",
                legend_title_text="Tipo de Peso"
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)

elif sst_input and not sst_valida:
    st.warning("⚠️ La SST debe contener exactamente 7 números para habilitar la matriz.")
else:
    st.info("💡 Ingrese la SST (7 números exactos) y seleccione el circuito para comenzar.")
