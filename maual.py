import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Caja Registradora de Manualidades", page_icon="🎨", layout="centered")

st.title("🎨 Control de Costos para Manualidades ✂️")
st.write("Selecciona los materiales que utilizaste para calcular el costo total de tu proyecto.")

# Inicializar el inventario base en la sesión para que no se borre al recargar
if "inventario" not in st.session_state:
    st.session_state.inventario = {
        "Fomix (Pliego)": 0.50,
        "Tijeras (Uso proporcional)": 0.10,
        "Silicona en barra": 0.25,
        "Goma líquida (Uso estimado)": 0.30,
        "Cartulina": 0.35,
        "Cinta de tela (Metro)": 0.60,
        "Escarcha / Brillantina": 0.40,
        "Ojitos locos (Par)": 0.15
    }

# Inicializar la lista de compras del usuario
if "compras" not in st.session_state:
    st.session_state.compras = []

# --- SECCIÓN A: AGREGAR NUEVOS MATERIALES AL INVENTARIO ---
with st.expander("➕ Agregar nuevo material a la lista de precios (Inventario)"):
    nuevo_nombre = st.text_input("Nombre del nuevo material (ej. Encaje, Caja de cartón):").strip()
    nuevo_precio = st.number_input("Precio por unidad ($):", min_value=0.0, step=0.05, format="%.2f")
    
    if st.button("Guardar material nuevo"):
        if nuevo_nombre:
            st.session_state.inventario[nuevo_nombre] = nuevo_precio
            st.success(f"¡Guardado! Ahora puedes seleccionar '{nuevo_nombre}' en la lista de abajo.")
        else:
            st.warning("Por favor, escribe un nombre válido.")

st.markdown("---")

# --- SECCIÓN B: REGISTRADORA DE MATERIALES USADOS ---
st.subheader("🛒 Registrar materiales usados en este proyecto")

col1, col2 = st.columns([2, 1])

with col1:
    material_seleccionado = st.selectbox(
        "Selecciona el material:",
        options=list(st.session_state.inventario.keys())
    )

with col2:
    cantidad = st.number_input("Cantidad:", min_value=1, value=1, step=1)

if st.button("✨ Agregar a la lista de consumo", use_container_width=True):
    precio_unitario = st.session_state.inventario[material_seleccionado]
    subtotal = precio_unitario * cantidad
    
    # Guardamos los datos de forma consistente
    st.session_state.compras.append({
        "Material": material_seleccionado,
        "Precio Unitario": float(precio_unitario),
        "Cantidad": int(cantidad),
        "Subtotal": float(subtotal)
    })

st.markdown("### 📋 Resumen del Proyecto Actual")

if st.session_state.compras:
    # Usamos st.dataframe con formato limpio
    st.dataframe(
        st.session_state.compras, 
        column_config={
            "Precio Unitario": st.column_config.NumberColumn(format="$%.2f"),
            "Subtotal": st.column_config.NumberColumn(format="$%.2f"),
        },
        use_container_width=True
    )
    
    # Calcular gran total
    total_proyecto = sum(item["Subtotal"] for item in st.session_state.compras)
    
    # Mostrar total destacado
    st.markdown(f"### 💰 **Costo Total de Materiales: ${total_proyecto:.2f}**")
    
    # Botón para limpiar todo
    if st.button("🗑️ Vaciar lista de materiales usados", type="primary"):
        st.session_state.compras = []
        if hasattr(st, "rerun"):
            st.rerun()
        else:
            st.experimental_rerun()
else:
    st.info("Aún no has agregado materiales. Selecciona arriba y presiona 'Agregar'.")
