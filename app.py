import streamlit as st

# Configuración de la pantalla para móviles
st.set_page_config(page_title="Meta Diaria 100%", page_icon="⚡", layout="centered")

st.title("⚡ Calculadora de Actividades")
st.write("Selecciona los trabajos planificados para ver si alcanzas el 100%.")

# Lista de actividades y sus pesos extraídos de tu imagen
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

# Crear una caja de selección múltiple
seleccionadas = st.multiselect(
    "Toca aquí para seleccionar las actividades:",
    options=list(actividades.keys())
)

st.divider()

# Calcular la suma
total_peso = sum([actividades[act] for act in seleccionadas])

# Mostrar el resultado grande
st.header(f"Total Acumulado: {total_peso}%")

# Barra de progreso visual (tope en 100%)
progreso_visual = min(total_peso, 100)
st.progress(progreso_visual / 100.0)

# Mensajes dependiendo de la puntuación
if total_peso == 0:
    st.info("Agrega actividades en la caja de arriba para comenzar.")
elif total_peso < 100:
    st.warning(f"Te faltan {100 - total_peso}% para llegar a la meta.")
else:
    st.success(f"¡Excelente! Has alcanzado y/o superado la meta diaria.")
    st.balloons() # Lanza globos de celebración en la pantalla
