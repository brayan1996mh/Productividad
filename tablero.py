import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import re

st.set_page_config(page_title="Productividad Definitiva ⚡", page_icon="⚡", layout="wide")

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

st.title("⚡ Tablero de Control Definitivo")

# Base de datos plana y robusta
CAPATACES = ["A. Aldonate", "A. Atoche", "A. Godoy", "A. Isuiza", "A. Torres", "A. Vigoria", "A. Villanueva", "C. Hernandez", "C. Mayaudon", "C. Ñaupas", "C. Padilla", "C. Salcedo", "D. Delgado", "D. Taquiri", "E. Ancco", "E. Antay", "E. Chihuan", "E. Diaz", "E. Flores", "E. La rosa", "F. Lozano", "F. Ramos", "H. Cabrera", "J. Abanto", "J. Apaza", "J. Arotinco", "J. Delgado", "J. Huari", "J. Panaifo", "J. Parra", "J. Salvador", "J. Suarez", "J. Villanueva", "L. Angeles", "L. Ayala", "L. Fiore", "M. Barrantes", "N. Pauro", "O. Aguilar", "P. Capcha", "R. Albites", "R. Rojas", "R. Torres", "S. Jacinto", "S. Lazaro", "V. Bordon", "V. Campos", "V. Orrillo", "V. Pérez", "V. Torres", "Y. Padilla"]

datos_completos = [
    ["AP", "Cable en cortocircuito de AP", 0.62], ["AP", "Cable a tierra AP", 0.23], ["SP", "Cable en cortocircuito de SP", 0.62], ["SP", "Cable a Tierra/ Electrizado SP", 0.52], ["AP", "Cable seccionado de AP", 0.59], ["AP", "Cable de AP dañado por terceros", 0.46], ["SP", "Cable seccionado De SP", 0.59], ["SP", "Cable de SP Dañado por terceros", 0.46], ["POSTES", "Cambio de poste chocado (con redes)", 0.77], ["POSTES", "Cambio de poste Corroído con redes", 0.77], ["POSTES", "Cambio de poste Corroído sin redes", 0.77], ["CNX", "Conexión Subterránea quemada de AP", 0.36], ["CNX", "Conexión Subterránea quemada de SP", 0.36], ["CNX", "Conexión subterránea sustraído o danado", 0.36], ["CNX", "Retiro de conexión subterránea por seguridad", 0.36], ["CNX", "Instalación de conexión subterránea con compromiso de pago", 0.31], ["CNX", "Conexión tipo IV quemada AP", 0.23], ["CNX", "Conexión Tipo IV quemada SP", 0.23], ["CNX", "Conexión Tipo IV Sustraída Danado", 0.23], ["CNX", "Instalación de Conexión tipo IV con compromiso de pago", 0.23], ["CNX", "Reparar falso contacto en conexión tipo IV", 0.23], ["CNX", "Retemplado de conexión tipo IV", 0.23], ["CNX", "Retiro de Conexión tipo IV por seguridad", 0.23], ["CNX", "Conexión Tipo V quemada SP (**)", 0.46], ["POSTES", "Enderezado de postes", 0.31], ["AP", "Red Aérea seccionada de AP", 0.27], ["SP", "Red Aérea caida De SP", 0.27], ["SP", "Red Aérea caida por choque", 0.27], ["SP", "Red Aérea seccionada de SP", 0.27], ["AP", "Red Aérea de AP Sustraída", 0.27], ["SP", "Cable de Comunicación Sustraído", 0.46], ["SP", "Cable de Subida Sustraído", 0.46], ["SP", "Cable Subterráneo Sustraído", 0.46], ["SP", "Red Aérea de AP y SP Sustraída", 0.27], ["SP", "Red Aérea de SP Sustraída", 0.27], ["AP", "Cambio de fotocélula", 0.46], ["AP", "Retiro de luminaria", 0.31], ["AP", "Cambio de Llave AP", 0.31], ["AP", "Red Aérea en cortocircuito", 0.27], ["AP", "Red Aérea seccionada por intento de hurto", 0.27], ["AP", "Reparación de falso contacto en red Aérea", 0.27], ["POSTES", "Reposición de poste chocado sin redes", 0.77], ["POSTES", "Reposición de poste corroído sin redes", 0.77], ["POSTES", "Retiro de poste chocado", 0.31], ["POSTES", "Retiro de poste corroído", 0.31], ["SP", "Cable de comunicación quemado", 0.46], ["SP", "Cambio de tablero de Distribución", 0.42], ["SP", "Levantar Líneas de Telef, Cable u Otros", 0.31], ["SP", "Retenida chocada", 0.31], ["SP", "Cambio de Llave BT", 0.31], ["SP", "Falso contacto disyuntor", 0.31], ["SP", "Profundizar cables", 0.31], ["SP", "Puenteo de Llaves AP", 0.31], ["SP", "Puenteo de Llaves BT", 0.31], ["SP", "Cambio de mástil", 0.23], ["SP", "Instalación de Tubos en Subidas Aéreas", 0.23], ["SP", "Reposición de contactor sustraído", 0.23], ["SP", "Verificar tablero aéreo BT", 0.22], ["SP", "Cambio de pasantes", 0.32], ["SP", "Cambio de murete", 0.31], ["SP", "Desoldado de tapas", 0.31], ["SP", "Otros Trabajos en Cajas Tomas", 0.31]
]
df_actividades = pd.DataFrame(datos_completos, columns=["CIRCUITO", "ACTIVIDAD", "PESO"])

# Selección
st.subheader("Datos Generales")
c1, c2 = st.columns(2)
fecha = c1.date_input("FECHA", value=date.today())
sst_input = c2.text_input("SST (7 números)")
sst_valida = bool(sst_input and re.match(r'^\d{7}$', sst_input))

c3, c4 = st.columns(2)
capataz = c3.selectbox("CAPATAZ", ["Seleccione..."] + CAPATACES)
lista_circuitos = ["Seleccione..."] + list(df_actividades["CIRCUITO"].unique())
circuito = c4.selectbox("CIRCUITO / SECTOR", lista_circuitos)

st.markdown("---")

if sst_valida and circuito != "Seleccione...":
    df_filtrado = df_actividades[df_actividades["CIRCUITO"] == circuito]
    opciones_act = df_filtrado["ACTIVIDAD"].tolist()
    seleccion = st.multiselect("Agregar trabajos:", opciones_act)

    if seleccion:
        st.markdown("---")
        st.subheader("Matriz de Avance")
        datos_reporte = []
        
        for act in seleccion:
            # Búsqueda infalible de peso
            peso_base = float(df_filtrado[df_filtrado["ACTIVIDAD"] == act]["PESO"].values[0])
            
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
