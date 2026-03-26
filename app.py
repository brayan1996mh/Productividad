import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import re

st.set_page_config(page_title="Tablero de Productividad ⚡", page_icon="⚡", layout="wide")

# Fondo Operacional
st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(180deg, rgba(5, 15, 25, 0.85) 0%, rgba(5, 10, 15, 0.95) 100%), 
                          url('https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=2000&auto=format&fit=crop');
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .stMarkdown, .stSubheader, .stTitle { text-shadow: 1px 1px 3px black; color: white; }
    input:disabled { color: #00E676 !important; -webkit-text-fill-color: #00E676 !important; font-weight: bold; background-color: rgba(0, 230, 118, 0.1) !important; border: 1px solid #00E676; }
    .stNumberInput div[data-baseweb="input"] input { color: #29B6F6 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Tablero de Control - Producción")

CAPATACES = ["A. Aldonate", "A. Atoche", "A. Godoy", "A. Isuiza", "A. Torres", "A. Vigoria", "A. Villanueva", "C. Hernandez", "C. Mayaudon", "C. Ñaupas", "C. Padilla", "C. Salcedo", "D. Delgado", "D. Taquiri", "E. Ancco", "E. Antay", "E. Chihuan", "E. Diaz", "E. Flores", "E. La rosa", "F. Lozano", "F. Ramos", "H. Cabrera", "J. Abanto", "J. Apaza", "J. Arotinco", "J. Delgado", "J. Huari", "J. Panaifo", "J. Parra", "J. Salvador", "J. Suarez", "J. Villanueva", "L. Angeles", "L. Ayala", "L. Fiore", "M. Barrantes", "N. Pauro", "O. Aguilar", "P. Capcha", "R. Albites", "R. Rojas", "R. Torres", "S. Jacinto", "S. Lazaro", "V. Bordon", "V. Campos", "V. Orrillo", "V. Pérez", "V. Torres", "Y. Padilla"]

# LÓGICA 1: Lista de actividades por circuito
ACTIVIDADES_POR_CIRCUITO = {
    "AP": ["Cable en cortocircuito de AP", "Cable a tierra AP", "Cable seccionado de AP", "Cable de AP dañado por terceros", "Red Aérea seccionada de AP", "Red Aérea de AP Sustraída", "Cambio de fotocélula", "Retiro de luminaria", "Cambio de Llave AP", "Red Aérea en cortocircuito", "Red Aérea seccionada por intento de hurto", "Reparación de falso contacto en red Aérea"],
    "SP": ["Cable en cortocircuito de SP", "Cable a Tierra/ Electrizado SP", "Cable seccionado De SP", "Cable de SP Dañado por terceros", "Red Aérea caida De SP", "Red Aérea caida por choque", "Red Aérea seccionada de SP", "Cable de Comunicación Sustraído", "Cable de Subida Sustraído", "Cable Subterráneo Sustraído", "Red Aérea de AP y SP Sustraída", "Red Aérea de SP Sustraída", "Cable de comunicación quemado", "Cambio de tablero de Distribución", "Levantar Líneas de Telef, Cable u Otros", "Retenida chocada", "Cambio de Llave BT", "Falso contacto disyuntor", "Profundizar cables", "Puenteo de Llaves AP", "Puenteo de Llaves BT", "Cambio de mástil", "Instalación de Tubos en Subidas Aéreas", "Reposición de contactor sustraído", "Verificar tablero aéreo BT", "Cambio de pasantes", "Cambio de murete", "Desoldado de tapas", "Otros Trabajos en Cajas Tomas"],
    "POSTES": ["Cambio de poste chocado (con redes)", "Cambio de poste Corroído con redes", "Cambio de poste Corroído sin redes", "Enderezado de postes", "Reposición de poste chocado sin redes", "Reposición de poste corroído sin redes", "Retiro de poste chocado", "Retiro de poste corroído"],
    "CNX": ["Conexión Subterránea quemada de AP", "Conexión Subterránea quemada de SP", "Conexión subterránea sustraído o danado", "Retiro de conexión subterránea por seguridad", "Instalación de conexión subterránea con compromiso de pago", "Conexión tipo IV quemada AP", "Conexión Tipo IV quemada SP", "Conexión Tipo IV Sustraída Danado", "Instalación de Conexión tipo IV con compromiso de pago", "Reparar falso contacto en conexión tipo IV", "Retemplado de conexión tipo IV", "Retiro de Conexión tipo IV por seguridad", "Conexión Tipo V quemada SP (**)"]
}

# LÓGICA 2: Diccionario Directo de Pesos (Imposible que de error de índice)
PESOS_DICT = {
    "Cable en cortocircuito de AP": 0.62, "Cable a tierra AP": 0.23, "Cable en cortocircuito de SP": 0.62, "Cable a Tierra/ Electrizado SP": 0.52, "Cable seccionado de AP": 0.59, "Cable de AP dañado por terceros": 0.46, "Cable seccionado De SP": 0.59, "Cable de SP Dañado por terceros": 0.46, "Cambio de poste chocado (con redes)": 0.77, "Cambio de poste Corroído con redes": 0.77, "Cambio de poste Corroído sin redes": 0.77, "Conexión Subterránea quemada de AP": 0.36, "Conexión Subterránea quemada de SP": 0.36, "Conexión subterránea sustraído o danado": 0.36, "Retiro de conexión subterránea por seguridad": 0.36, "Instalación de conexión subterránea con compromiso de pago": 0.31, "Conexión tipo IV quemada AP": 0.23, "Conexión Tipo IV quemada SP": 0.23, "Conexión Tipo IV Sustraída Danado": 0.23, "Instalación de Conexión tipo IV con compromiso de pago": 0.23, "Reparar falso contacto en conexión tipo IV": 0.23, "Retemplado de conexión tipo IV": 0.23, "Retiro de Conexión tipo IV por seguridad": 0.23, "Conexión Tipo V quemada SP (**)": 0.46, "Enderezado de postes": 0.31, "Red Aérea seccionada de AP": 0.27, "Red Aérea caida De SP": 0.27, "Red Aérea caida por choque": 0.27, "Red Aérea seccionada de SP": 0.27, "Red Aérea de AP Sustraída": 0.27, "Cable de Comunicación Sustraído": 0.46, "Cable de Subida Sustraído": 0.46, "Cable Subterráneo Sustraído": 0.46, "Red Aérea de AP y SP Sustraída": 0.27, "Red Aérea de SP Sustraída": 0.27, "Cambio de fotocélula": 0.46, "Retiro de luminaria": 0.31, "Cambio de Llave AP": 0.31, "Red Aérea en cortocircuito": 0.27, "Red Aérea seccionada por intento de hurto": 0.27, "Reparación de falso contacto en red Aérea": 0.27, "Reposición de poste chocado sin redes": 0.77, "Reposición de poste corroído sin redes": 0.77, "Retiro de poste chocado": 0.31, "Retiro de poste corroído": 0.31, "Cable de comunicación quemado": 0.46, "Cambio de tablero de Distribución": 0.42, "Levantar Líneas de Telef, Cable u Otros": 0.31, "Retenida chocada": 0.31, "Cambio de Llave BT": 0.31, "Falso contacto disyuntor": 0.31, "Profundizar cables": 0.31, "Puenteo de Llaves AP": 0.31, "Puenteo de Llaves BT": 0.31, "Cambio de mástil": 0.23, "Instalación de Tubos en Subidas Aéreas": 0.23, "Reposición de contactor sustraído": 0.23, "Verificar tablero aéreo BT": 0.22, "Cambio de pasantes": 0.32, "Cambio de murete": 0.31, "Desoldado de tapas": 0.31, "Otros Trabajos en Cajas Tomas": 0.31
}

st.subheader("Datos Generales")
c1, c2 = st.columns(2)
fecha = c1.date_input("FECHA", value=date.today())
sst_input = c2.text_input("SST (7 números)")
sst_valida = bool(sst_input and re.match(r'^\d{7}$', sst_input))

c3, c4 = st.columns(2)
capataz = c3.selectbox("CAPATAZ", ["Seleccione..."] + CAPATACES)
circuito = c4.selectbox("CIRCUITO / SECTOR", ["Seleccione..."] + list(ACTIVIDADES_POR_CIRCUITO.keys()))

st.markdown("---")

if sst_valida and circuito != "Seleccione...":
    opciones_act = ACTIVIDADES_POR_CIRCUITO[circuito]
    seleccion = st.multiselect("Agregar trabajos:", opciones_act)

    if seleccion:
        st.markdown("---")
        st.subheader("Matriz de Avance")
        datos_reporte = []
        
        for act in seleccion:
            # LÓGICA 3: Llamada directa al diccionario usando .get(). Nunca se rompe.
            peso_base = PESOS_DICT.get(act, 0.0)
            
            with st.container():
                st.write(f"### 🔧 {act}")
                col1, col2, col3, col4 = st.columns(4)
                estado = col1.selectbox("Estado", ["Finalizado", "Devuelto", "Pendiente"], key=f"e_{act}")
                col2.text_input("Peso Base", value=f"{peso_base}%", disabled=True, key=f"b_{act}")
                avance = col3.number_input("Avance (%)", 0, 100, 100, 10, key=f"a_{act}", format="%d%%")
                peso_real = (avance / 100) * peso_base
                col4.text_input("Peso Real", value=f"{peso_real:.2f}%", disabled=True, key=f"r_{act}")
                datos_reporte.append({"Act": act, "Base": peso_base, "Real": peso_real})
        
        if datos_reporte:
            total_real = sum(d["Real"] for d in datos_reporte)
            st.markdown("---")
            
            c_gauge, c_info = st.columns([2, 1])
            with c_gauge:
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number", value=total_real, title={'text': "Producción (%)", 'font': {'color': "white"}},
                    gauge={'axis': {'range': [0, 120], 'tickcolor': "white"}, 'bar': {'color': "#00E676" if total_real >= 100 else "#FFEB3B"}, 'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}}
                ))
                fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
                st.plotly_chart(fig_g, use_container_width=True)
            
            with c_info:
                st.metric("Puntaje", f"{total_real:.2f}%")
                if total_real >= 100: st.success("✅ Meta alcanzada")
                else: st.warning(f"Falta {(100-total_real):.2f}%")

            st.write("### Comparativo")
            fig_b = go.Figure(data=[
                go.Bar(name='Base', x=[d["Act"] for d in datos_reporte], y=[d["Base"] for d in datos_reporte], marker_color='#B0BEC5'),
                go.Bar(name='Real', x=[d["Act"] for d in datos_reporte], y=[d["Real"] for d in datos_reporte], marker_color='#0288D1')
            ])
            fig_b.update_layout(barmode='group', template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_tickangle=-45)
            st.plotly_chart(fig_b, use_container_width=True)

elif sst_input and not sst_valida:
    st.error("⚠️ Ingrese exactamente 7 números en la SST.")
