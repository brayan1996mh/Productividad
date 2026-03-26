import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random

# Configuración de la página (Layout ancho para mejor manejo táctil)
st.set_page_config(page_title="Gestión Pro Diaria AP ⚡", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# 1. ESTILO PROFESIONAL Y SUBTIL (CSS)
styl = f"""
<style>
    /* Estilo para el fondo (Background de esquemas eléctricos sutil) */
    .stApp {{
        background-image: linear-gradient(180deg, rgba(0,0,0,0.85) 0%, rgba(10,30,50,0.92) 100%), 
                          url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAnIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgMzAwIDMwMCI+PHBhdGggZD0iTTAgMGgzMDB2MzAwSDB6IiBmaWxsPSJub25lIi8+PHBhdGggZD0iTTEwMCAxMDBoMTB2MTBoLTEwek0xNDAgMTAwaDEwdjEwaC0xMHpNMTgwIDEwMGgxMHYxMGgtMTB6TTIwMCAxMDBoMTB2MTBoLTEwek0yNDAgMTAwaDEwdjEwaC0xMHpNMTAwIDE4MGgxMHYxMGgtMTB6TTE0MCAxODBoMTB2MTBoLTEwek0xODAgMTgwaDEwdjEwaC0xMHpNMjAwIDE4MGgxMHYxMGgtMTB6TTI0MCAxODBoMTB2MTBoLTEwek0xMDAgMjQwaDEwdjEwaC0xMHpNMTQwIDI0MGgxMHYxMGgtMTB6TTE4MCAyNDBoMTB2MTBoLTEwek0yMDAgMjQwaDEwdjEwaC0xMHpNMjQwIDI0MGgxMHYxMGgtMTB6TTEwMCAzMDBoMTB2MTBoLTEwek0xNDAgMzAwSDB2LTE5NjhIMHoiIGZpbGw9Im5vbmUiLz48cGF0aCBkPSJNMCAwYzIuNDU4IDAgNC45MjEuMTM5IDcuMzc1LjQwOEw5Ny43MjUgOTEuMTVMMTYyLjcwNSA5M3MyNDUuNTQxIDExOC4wNjcgMjc4LjY5OCAxNTkuNjUyQzE1MC40MDQgMTg5LjY4IDkwLjgzMiAyNDkuMjUyIDAgMzAwY0MgLTQ4Ljg5OCA0MC43MDcgLTg4Ljc4NyA4OC43ODcgLTg4Ljc4N2MxNC44NDYgMCAyOS4wMTQgMy45MzggNDEuNzY0IDEwLjc3OEM3Ny43MDkgMTkyLjc5NCA0MC43MDcgMTU2LjAwNCAwIDM4NS43NEMwIDMwMCAtNDUuNzA5IDI3OS4wMzYgLTk1LjUzMSAyMzY4LjU4NEMxNzYuOTczIDI0NS41NDEgMjUuNTQxIDk1LjMzMSB6IiBmaWxsPSIjMDcwMDNiMjMiLz48L3N2Zz4=');
        background-size: 400px;
        background-repeat: repeat;
        background-blend-mode: multiply;
    }}

    /* Compactación de márgenes táctiles */
    .stMarkdown, .stSubheader, .stTitle {{
        margin-top: -10px !important;
        margin-bottom: 2px !important;
    }}

    /* Compactación del bloque de tareas (Paso 2) */
    .stForm {{
        padding: 5px !important;
        border-radius: 8px !important;
    }}

    /* Estilo para las cabeceras de columna de datos táctiles */
    [data-testid="stHorizontalBlock"] .stMarkdown {{
        color: #B0BEC5 !important;
        font-weight: bold;
        margin-bottom: -5px !important;
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
    # 2. REPORTE DE CAMPO OPERATIVO (Layout Ultra Compacto para Móvil)
    st.subheader("Paso 2: Reporte de Campo (Dinámico y Táctil)")
    st.caption("El `% Peso Real` se calcula al instante de ajustar el deslizador de avance.")
    
    # Cabeceras de columna para los datos táctiles
    st.write("") # Espaciador profesional
    cH1, cH2, cH3 = st.columns([1.5, 3, 1.5]) # Proporciones de columna dactilar
    cH1.write("##### Estado")
    cH2.write("##### % Avance (0-100%)")
    cH3.write("##### % Peso Real")
    
    datos_reporte = []
    total_base_peso = 0
    
    # Creamos las "tarjetas" compactas
    for act in seleccionadas:
        with st.container():
            # Título de actividad encíma
            st.write(f"#### 🔧 {act}")
            
            # Tres columnas en una sola fila para compactar el espacio vertical en móvil
            col1, col2, col3 = st.columns([1.5, 3, 1.5]) 
            
            # Columna 1: Estado táctil (selectbox)
            with col1:
                # Opciones compactas: Finalizado o Devuelto
                estado = st.selectbox("Estado", ["Finalizado", "Devuelto"], key=f"est_{act}", label_visibility="collapsed")
            
            # Columna 2: Avance táctil (slider con step de 5% para rapidez dactilar)
            with col2:
                # Comportamiento automático: si Finalizado -> 100%, si Devuelto -> 50% por defecto
                avance_default = 100 if estado == "Finalizado" else 50
                avance = st.slider("% Avance", min_value=0, max_value=100, value=avance_default, step=5, key=f"av_{act}", label_visibility="collapsed")
            
            # Columna 3: Peso Obtenido (Cálculo automático en Metric compacto)
            with col3:
                # Cálculo automático en tiempo real
                peso_real = (avance / 100.0) * actividades[act]
                # Usamos st.metric formateado profesionalmente
                st.metric("Peso Obtenido", f"{peso_real:.1f}%", help="Cálculo automático: Peso Base * % Avance / 100")
            
            # Un pequeño espaciador profesional
            st.divider()
            
            # Guardamos los datos para los gráficos
            datos_reporte.append({
                "Actividad": act,
                "Peso Base": actividades[act],
                "Estado": estado,
                "Avance": avance,
                "Peso Real": peso_real
            })
            total_base_peso += actividades[act]
            
    # Convertimos los datos a una tabla (DataFrame)
    df_reporte = pd.DataFrame(datos_reporte)
    
    # 3. DASHBOARD DE CUMPLIMIENTO OPERATIVO (PROFESIONAL Y ROBUSTO)
    if not df_reporte.empty:
        st.markdown("---")
        st.subheader("Paso 3: Dashboard de Avance Operativo")
        total_peso_real = df_reporte["Peso Real"].sum()
        
        # Gráfico 1: Medidor tipo Velocímetro Eléctrico
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = total_peso_real,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Avance Real Acumulado del Día", 'font': {'size': 24, 'color': "white"}},
            gauge = {
                'axis': {'range': [0, 150], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#00E676" if total_peso_real >= 100 else "#29B6F6"}, # Verde si llega a 100, azul si falta
                'bgcolor': "black",
                'borderwidth': 1,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 100], 'color': "#ffebee1A"} # Zona de cumplimiento (10% opacidad)
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 3},
                    'thickness': 0.75,
                    'value': 100 # Meta del 100%
                }
            },
            number = {'suffix': "%", 'font': {'size': 40, 'color': "white"}}
        ))
        
        # Gráfico 2: Barras Interactivas (Planificado vs Real)
        fig_bar = px.bar(
            df_reporte, x="Actividad", y=["Peso Base", "Peso Real"], 
            barmode='group', 
            labels={'value': '% Peso Diario'},
            template="plotly_dark", # Tema oscuro para que combine
            color_discrete_sequence=["#B0BEC5", "#0288D1"] # Gris para el plan, Azul fuerte para lo real
        )
        # Inclina los textos para que se lean bien en móvil
        fig_bar.update_layout(xaxis_tickangle=-45, yaxis=dict(range=[0, max(120, total_peso_real)])) 
        
        # Mostrar gráficos en columnas (50/50 en desktop, se apilan en móvil)
        colCharts1, colCharts2 = st.columns(2)
        with colCharts1:
            st.plotly_chart(fig_gauge, use_container_width=True)
        with colCharts2:
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Resumen y Alertas (Eliminado st.balloons)
        if total_peso_real >= 100:
            st.success(f"⚡ Objetivo Cumplido: La cuadrilla alcanzó un {total_peso_real:.1f}% real acumulado.")
        else:
            st.warning(f"⚠️ Atención: Cumplimiento al {total_peso_real:.1f}%. Faltan {100 - total_peso_real:.1f}% real para cerrar la meta diaria.")
            
else:
    st.info("👆 Selecciona los trabajos programados en la lista desplegable superior para iniciar el reporte táctil.")
