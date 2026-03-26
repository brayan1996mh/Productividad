import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuración de la página (Layout ancho para mejor manejo de tabla)
st.set_page_config(page_title="Gestión Pro Diaria AP ⚡", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# 1. ESTILO PROFESIONAL Y SUBTIL (CSS)
styl = f"""
<style>
    /* Estilo para el fondo (Background de esquemas eléctricos sutil) */
    .stApp {{
        background-image: linear-gradient(180deg, rgba(0,0,0,0.85) 0%, rgba(10,30,50,0.92) 100%), 
                          url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAnIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgMzAwIDMwMCI+PHBhdGggZD0iTTAgMGgzMDB2MzAwSDB6IiBmaWxsPSJub25lIi8+PHBhdGggZD0iTTEwMCAxMDBoMTB2MTBoLTEwek0xNDAgMTAwaDEwdjEwaC0xMHpNMTgwIDEwMGgxMHYxMGgtMTB6TTIwMCAxMDBoMTB2MTBoLTEwek0yNDAgMTAwaDEwdjEwaC0xMHpNMTAwIDE0MGgxMHYxMGgtMTB6TTE4MCAxNDBoMTB2MTBoLTEwek0yMDAgMTQwaDEwdjEwaC0xMHpNMjQwIDE0MGgxMHYxMGgtMTB6TTEwMCAxODB4MTB2MTBoLTEwek0xNDAgMTgwSDB2LTE5NjhIMHoiIGZpbGw9Im5vbmUiLz48cGF0aCBkPSJNMCAwYzIuNDU4IDAgNC45MjEuMTM5IDcuMzc1LjQwOEw5Ny43MjUgOTEuMTVMMTYyLjcwNSA5M3MyNDUuNTQxIDExOC4wNjcgMjc4LjY5OCAxNTkuNjUyQzE1MC40MDQgMTg5LjY4IDkwLjgzMiAyNDkuMjUyIDAgMzAwY0MgLTQ4Ljg5OCA0MC43MDcgLTg4Ljc4NyA4OC43ODcgLTg4Ljc4N2MxNC44NDYgMCAyOS4wMTQgMy45MzggNDEuNzY0IDEwLjc3OEM3Ny43MDkgMTkyLjc5NCA0MC43MDcgMTU2LjAwNCAwIDM4NS43NEMwIDMwMCAtNDUuNzA5IDI3OS4wMzYgLTk1LjUzMSAyMzY4LjU4NEMxNzYuOTczIDI0NS41NDEgMjUuNTQxIDk1LjMzMSB6IiBmaWxsPSIjMDcwMDNiMjMiLz48L3N2Zz4=');
        background-size: 400px;
        background-repeat: repeat;
        background-blend-mode: multiply;
    }}

    /* Compactación de márgenes táctiles */
    .stMarkdown, .stSubheader, .stTitle {{
        margin-top: -10px !important;
        margin-bottom: 2px !important;
    }}

    /* Estilo profesional para métricas */
    [data-testid="stMetricValue"] {{
        font-size: 1.5rem !important;
        color: #00E676 !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 0.9rem !important;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

st.title("⚡ Panel de Gestión Pro de Cuadrillas AP")
st.caption("Uso exclusivo para Personal Operativo en Campo")
st.markdown("---")

# Diccionario de actividades y pesos
actividades = {
    "Cable en cortocircuito de AP": 62,
    "Cable seccionado de AP": 59,
    "Cable de AP dañado por terceros": 46,
    "Cambio de fotocélula": 46,
    "Retiro de luminaria": 31,
    "Cambio de Llave AP": 31,
    "Red Aérea seccionada de AP": 27,
    "Red Aérea de AP Sustraída": 27,
    "Red Aérea en cortocircuito": 27,
    "Red Aérea seccionada por intento de hurto": 27,
    "Reparación de falso contacto en red Aérea": 27,
    "Cable a tierra AP": 23
}

# 1. SELECCIÓN DE TRABAJOS (Compactada)
st.subheader("Paso 1: Selección del Plan Operativo")
seleccionadas = st.multiselect(
    "Toca para agregar trabajos al plan del día:", 
    options=list(actividades.keys()),
    label_visibility="collapsed"
)

if seleccionadas:
    st.markdown("---")
    # 2. REPORTE DE CAMPO OPERATIVO (Layout Tabla Táctil)
    st.subheader("Paso 2: Reporte de Campo (Dinámico y Táctil)")
    st.caption("Ingresa el avance numérico en las casillas. El `% Peso Real` se calcula al instante.")
    
    # Cabeceras de columna fijas tipo Tabla
    st.write("") 
    cH1, cH2, cH3, cH4, cH5 = st.columns([2.5, 1.5, 1.5, 1.5, 1.5]) 
    cH1.write("##### Actividad")
    cH2.write("##### Estado")
    cH3.write("##### % Peso Base")
    cH4.write("##### % Avance (0-100)")
    cH5.write("##### % Peso Real")
    
    datos_reporte = []
    total_base_peso = 0
    
    # Creamos las filas compactas de la tabla
    for act in seleccionadas:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2.5, 1.5, 1.5, 1.5, 1.5]) 
            
            # Columna 1: Nombre de Actividad
            with col1:
                st.write(f"🔧 **{act}**")
            
            # Columna 2: Estado táctil (Solo las 3 opciones requeridas)
            with col2:
                estado = st.selectbox("Estado", ["Finalizado", "Devuelto", "Indebido"], key=f"est_{act}", label_visibility="collapsed")
            
            # Columna 3: Peso Base (Estático y bloqueado)
            with col3:
                st.metric("% Peso Base", f"{actividades[act]}%", label_visibility="collapsed")
            
            # Columna 4: Avance (Casilla en blanco/0%, solo permite números)
            with col4:
                avance = st.number_input("% Avance", min_value=0, max_value=100, value=0, step=10, key=f"av_{act}", label_visibility="collapsed")
            
            # Columna 5: Peso Obtenido (Cálculo automático)
            with col5:
                peso_real = (avance / 100.0) * actividades[act]
                st.metric("% Peso Real", f"{peso_real:.1f}%", help="Cálculo automático: Peso Base * % Avance / 100", label_visibility="collapsed")
            
            datos_reporte.append({
                "Actividad": act,
                "Peso Base": actividades[act],
                "Estado": estado,
                "Avance": avance,
                "Peso Real": peso_real
            })
            total_base_peso += actividades[act]
            
    df_reporte = pd.DataFrame(datos_reporte)
    
    # 3. DASHBOARD DE CUMPLIMIENTO (CORREGIDO)
    if not df_reporte.empty:
        st.markdown("---")
        st.subheader("Paso 3: Dashboard de Avance Operativo")
        total_peso_real = df_reporte["Peso Real"].sum()
        
        # Gráfico 1: Velocímetro (Con el error de color arreglado)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = total_peso_real,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Avance Real Acumulado", 'font': {'size': 24, 'color': "white"}},
            gauge = {
                'axis': {'range': [0, 150], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#00E676" if total_peso_real >= 100 else "#29B6F6"}, 
                'bgcolor': "black",
                'borderwidth': 1,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 100], 'color': "rgba(255, 235, 238, 0.1)"} # <--- ¡AQUÍ ESTABA EL ERROR! Ya está solucionado.
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 3},
                    'thickness': 0.75,
                    'value': 100 
                }
            },
            number = {'suffix': "%", 'font': {'size': 40, 'color': "white"}}
        ))
        
        # Gráfico 2: Barras
        fig_bar = px.bar(
            df_reporte, x="Actividad", y=["Peso Base", "Peso Real"], 
            barmode='group', 
            labels={'value': '% Peso Diario'},
            template="plotly_dark", 
            color_discrete_sequence=["#B0BEC5", "#0288D1"] 
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
    st.info("👆 Selecciona los trabajos programados en la lista desplegable superior para iniciar el reporte.")
