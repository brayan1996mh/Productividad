import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

# Configuración de la página
st.set_page_config(page_title="Productividad Emergencias ⚡", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# 1. ESTILO PROFESIONAL Y SUBTIL (CSS)
styl = f"""
<style>
    .stApp {{
        background-image: linear-gradient(180deg, rgba(0,0,0,0.85) 0%, rgba(10,30,50,0.92) 100%), 
                          url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAnIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgMzAwIDMwMCI+PHBhdGggZD0iTTAgMGgzMDB2MzAwSDB6IiBmaWxsPSJub25lIi8+PHBhdGggZD0iTTEwMCAxMDBoMTB2MTBoLTEwek0xNDAgMTAwaDEwdjEwaC0xMHpNMTgwIDEwMGgxMHYxMGgtMTB6TTIwMCAxMDBoMTB2MTBoLTEwek0yNDAgMTAwaDEwdjEwaC0xMHpNMTAwIDE0MGgxMHYxMGgtMTB6TTE4MCAxNDBoMTB2MTBoLTEwek0yMDAgMTQwaDEwdjEwaC0xMHpNMjQwIDE0MGgxMHYxMGgtMTB6TTEwMCAxODB4MTB2MTBoLTEwek0xNDAgMTgwSDB2LTE5NjhIMHoiIGZpbGw9Im5vbmUiLz48cGF0aCBkPSJNMCAwYzIuNDU4IDAgNC45MjEuMTM5IDcuMzc1LjQwOEw5Ny43MjUgOTEuMTVMMTYyLjcwNSA5M3MyNDUuNTQxIDExOC4wNjcgMjc4LjY5OCAxNTkuNjUyQzE1MC40MDQgMTg5LjY4IDkwLjgzMiAyNDkuMjUyIDAgMzAwY0MgLTQ4Ljg5OCA0MC43MDcgLTg4Ljc4NyA4OC43ODcgLTg4Ljc4N2MxNC44NDYgMCAyOS4wMTQgMy45MzggNDEuNzY0IDEwLjc3OEM3Ny43MDkgMTkyLjc5NCA0MC43MDcgMTU2LjAwNCAwIDM4NS43NEMwIDMwMCAtNDUuNzA5IDI3OS4wMzYgLTk1LjUzMSAyMzY4LjU4NEMxNzYuOTczIDI0NS41NDEgMjUuNTQxIDk1LjMzMSB6IiBmaWxsPSIjMDcwMDNiMjMiLz48L3N2Zz4=');
        background-size: 400px;
        background-repeat: repeat;
        background-blend-mode: multiply;
    }}
    .stMarkdown, .stSubheader, .stTitle {{
        margin-top: -10px !important;
        margin-bottom: 2px !important;
    }}
    /* Forzar el color verde y actualización visual en inputs deshabilitados */
    input:disabled {{
        color: #00E676 !important;
        -webkit-text-fill-color: #00E676 !important;
        font-weight: bold;
        background-color: rgba(0, 230, 118, 0.05) !important;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

# 2. CARGA INTELIGENTE DE DATOS
@st.cache_data
def cargar_datos():
    try:
        # AQUI ESTÁN LOS NOMBRES EXACTOS DE TUS ARCHIVOS
        df_act = pd.read_csv('Actividades emergencias.xlsx - Hoja1.csv')
        df_cap = pd.read_csv('Capataces Emergencias.xlsx - Hoja1.csv')
        
        # Normalizar nombres de columnas a mayúsculas
        df_act.columns = df_act.columns.str.strip().str.upper()
        df_cap.columns = df_cap.columns.str.strip().str.upper()
        
        # Encontrar las columnas dinámicamente
        col_circuito = [c for c in df_act.columns if 'CIRCUITO' in c][0]
        col_actividad = [c for c in df_act.columns if 'ACTIV' in c][0]
        col_peso = [c for c in df_act.columns if 'PESO' in c][0]
        
        # Limpiar datos
        df_act = df_act.dropna(subset=[col_circuito, col_actividad])
        lista_capataces = df_cap.iloc[:, 0].dropna().unique().tolist()
        
        return df_act, lista_capataces, col_circuito, col_actividad, col_peso
    except Exception as e:
        return None, None, None, None, None

df_act, lista_capataces, col_circuito, col_actividad, col_peso = cargar_datos()

st.title("⚡ Tablero de Control de Productividad - Emergencias")
st.markdown("---")

if df_act is None:
    st.error("⚠️ No se encontraron los archivos CSV. Por favor, sube 'Actividades emergencias.xlsx - Hoja1.csv' y 'Capataces Emergencias.xlsx - Hoja1.csv' a tu GitHub.")
    st.stop()

# 3. ENCABEZADO: DATOS DEL REPORTE
st.subheader("Datos Generales")
col_f, col_s = st.columns(2)
fecha_seleccionada = col_f.date_input("FECHA", value=date.today())
sst_ingresado = col_s.text_input("SST")

col_cap, col_cir = st.columns(2)
# Menú desplegable de Capataces
capataz_seleccionado = col_cap.selectbox("CAPATAZ", ["Seleccione un capataz..."] + lista_capataces)

# Menú desplegable de Circuitos
lista_circuitos = df_act[col_circuito].unique().tolist()
circuito_seleccionado = col_cir.selectbox("CIRCUITO", ["Seleccione un circuito..."] + lista_circuitos)

st.markdown("---")

# 4. SELECCIÓN DE ACTIVIDADES (Dependiente del Circuito)
st.subheader("Selección de Actividades Asignadas")

if circuito_seleccionado != "Seleccione un circuito...":
    # Filtrar actividades según el circuito elegido
    actividades_filtradas = df_act[df_act[col_circuito] == circuito_seleccionado]
    lista_actividades = actividades_filtradas[col_actividad].tolist()
    
    actividades_seleccionadas = st.multiselect(
        "Toca para agregar trabajos al plan del día:", 
        options=lista_actividades,
        label_visibility="collapsed"
    )

    if actividades_seleccionadas:
        st.markdown("---")
        # 5. MATRIZ DE PRODUCTIVIDAD
        st.subheader("Matríz de Productividad")
        
        datos_reporte = []
        
        for act in actividades_seleccionadas:
            with st.container():
                st.write(f"### 🔧 {act}")
                
                # Obtener el peso base
                peso_base_val = actividades_filtradas[actividades_filtradas[col_actividad] == act][col_peso].values[0]
                if isinstance(peso_base_val, str):
                    peso_base_val = float(peso_base_val.replace('%', '').strip())
                
                col1, col2, col3, col4 = st.columns(4) 
                
                with col1:
                    estado = st.selectbox("Estado", ["", "Finalizado", "Devuelto", "Indebido"], key=f"est_{act}")
                
                with col2:
                    st.text_input("% Peso Base", value=f"{peso_base_val}%", disabled=True, key=f"base_{act}")
                
                with col3:
                    avance = st.number_input("% Avance (0-100)", min_value=0, max_value=100, value=0, step=10, key=f"av_{act}")
                
                with col4:
                    peso_real = (avance / 100.0) * float(peso_base_val)
                    # Casilla sin key para forzar actualización dinámica en Streamlit
                    st.text_input("% Peso Real", value=f"{peso_real:.1f}%", disabled=True)
                
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
                
                datos_reporte.append({
                    "Actividad": act,
                    "Peso Base": peso_base_val,
                    "Estado": estado,
                    "Avance": avance,
                    "Peso Real": peso_real
                })
                
        df_reporte = pd.DataFrame(datos_reporte)
        
        # 6. DASHBOARD DE AVANCE DE PRODUCCIÓN
        if not df_reporte.empty:
            st.subheader("Dashboard de Avance de Producción")
            total_peso_real = df_reporte["Peso Real"].sum()
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_peso_real,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Avance Real Acumulado", 'font': {'size': 24, 'color': "white"}},
                gauge = {
                    'axis': {'range': [0, max(150, total_peso_real + 20)], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#00E676" if total_peso_real >= 100 else "#29B6F6"}, 
                    'bgcolor': "black",
                    'borderwidth': 1,
                    'bordercolor': "gray",
                    'steps': [{'range': [0, 100], 'color': "rgba(255, 235, 238, 0.1)"}],
                    'threshold': {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 100}
                },
                number = {'suffix': "%", 'font': {'size': 40, 'color': "white"}}
            ))
            
            fig_bar = px.bar(
                df_reporte, x="Actividad", y=["Peso Base", "Peso Real"], 
                barmode='group', labels={'value': '% Peso Diario'},
                template="plotly_dark", color_discrete_sequence=["#B0BEC5", "#0288D1"] 
            )
            fig_bar.update_layout(xaxis_tickangle=-45, yaxis=dict(range=[0, max(120, total_peso_real)])) 
            
            colCharts1, colCharts2 = st.columns(2)
            with colCharts1:
                st.plotly_chart(fig_gauge, use_container_width=True)
            with colCharts2:
                st.plotly_chart(fig_bar, use_container_width=True)
            
            if total_peso_real >= 100:
                st.success(f"⚡ Objetivo Cumplido: La cuadrilla alcanzó un {total_peso_real:.1f}% real acumulado.")
            else:
                st.warning(f"⚠️ Atención: Cumplimiento al {total_peso_real:.1f}%. Faltan {100 - total_peso_real:.1f}% real para cerrar la meta diaria.")
else:
    st.info("👆 Selecciona un Circuito primero para cargar las actividades correspondientes.")
