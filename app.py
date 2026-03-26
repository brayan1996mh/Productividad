import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuración de página más ancha para los gráficos
st.set_page_config(page_title="Gestión de Cuadrillas ⚡", page_icon="⚡", layout="wide")

st.title("⚡ Panel de Control Operativo AP")
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

st.subheader("1. Selección de Trabajos")
seleccionadas = st.multiselect(
    "Selecciona las actividades planificadas para la jornada:", 
    options=list(actividades.keys())
)

if seleccionadas:
    st.markdown("---")
    st.subheader("2. Reporte de Campo (Interactivo)")
    st.caption("Ajusta el estado y el avance táctil para calcular el peso real.")
    
    datos_reporte = []
    
    # Creamos un formulario dinámico y amigable para el móvil por cada actividad
    for act in seleccionadas:
        with st.container():
            st.markdown(f"**🔧 {act}** | Peso Plan: `{actividades[act]}%`")
            # 3 columnas para que encaje perfecto en la pantalla del capataz
            col1, col2, col3 = st.columns(3)
            
            estado = col1.selectbox("Estado", ["Finalizado", "Devuelto"], key=f"est_{act}")
            
            # Si el capataz marca finalizado, por defecto le damos 100%. Si es devuelto, 50%.
            avance_default = 100 if estado == "Finalizado" else 50
            avance = col2.number_input("% Avance", min_value=0, max_value=100, value=avance_default, step=5, key=f"av_{act}")
            
            # Cálculo automático en tiempo real
            peso_real = (avance / 100.0) * actividades[act]
            col3.metric("Peso Real Obtenido", f"{peso_real:.1f}%")
            
            # Guardamos los datos en la memoria para los gráficos
            datos_reporte.append({
                "Actividad": act,
                "Peso Base": actividades[act],
                "Estado": estado,
                "Avance": avance,
                "Peso Real": peso_real
            })
            st.write("") # Espaciador visual
            
    # Convertimos los datos a una tabla (DataFrame)
    df_reporte = pd.DataFrame(datos_reporte)
    total_peso_real = df_reporte["Peso Real"].sum()
    
    st.markdown("---")
    st.subheader("3. Dashboard de Cumplimiento")
    
    # Gráfico 1: Medidor tipo Velocímetro Tecnológico
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_peso_real,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Avance Real Acumulado (%)", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, max(120, total_peso_real)], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#00E676" if total_peso_real >= 100 else "#29B6F6"}, # Verde si llega a 100, azul si falta
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 80], 'color': "#ffebee"},  # Rojo claro (Peligro)
                {'range': [80, 100], 'color': "#fff9c4"} # Amarillo (Cerca)
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100 # La línea roja es la meta del 100%
            }
        }
    ))
    
    # Gráfico 2: Barras Interactivas (Planificado vs Real)
    fig_bar = px.bar(
        df_reporte, x="Actividad", y=["Peso Base", "Peso Real"], 
        barmode='group', 
        title="Brecha: Peso Planificado vs. Ejecutado",
        color_discrete_sequence=["#B0BEC5", "#0288D1"] # Gris para el plan, Azul fuerte para lo real
    )
    fig_bar.update_layout(xaxis_tickangle=-45) # Inclina los textos para que se lean bien en móvil
    
    # Mostrar gráficos
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Resumen y Alertas
    if total_peso_real >= 100:
        st.success(f"⚡ ¡Objetivo Cumplido! La cuadrilla alcanzó un {total_peso_real:.1f}%.")
        st.balloons()
    else:
        st.warning(f"⚠️ Atención: Cumplimiento al {total_peso_real:.1f}%. Faltan {100 - total_peso_real:.1f}% para cerrar la meta diaria.")
        
else:
    st.info("👆 Selecciona los trabajos programados en la lista desplegable superior para iniciar el reporte.")
