import streamlit as st
import os
import json

# Configuración de la página
st.set_page_config(page_title="Caja Registradora de Manualidades", page_icon="🎨", layout="centered")

st.title("🎨 Control de Costos para Manualidades MISHELL 💖🍷💋")
st.write("Selecciona los materiales que utilizaste para calcular el costo total de tu proyecto.")

# --- CONTROL DE INVENTARIO PERMANENTE ---
# Definimos un archivo oculto para guardar los precios permanentemente
ARCHIVO_INVENTARIO = "inventario_permanente.json"

# Tu lista base por defecto (si el archivo aún no existe)
inventario_base = {
    "Carpeta Tapa Tranparente A3": 2.61,
    "Carton (Paquete A3) 5 UNIDADES": 1.94,
    "Carton (Paquete A4) 10 UNIDADES": 1.18,
    "Carton (Pliego Delgado)": 1.00,
    "Carton (Pliego Grueso)": 1.37,
    "Cartulina Escarchada(Paquete)": 1.18,
    "Cartulina(Paquete)": 0.92,
    "Cinta": 1.84,
    "Cinta de embalaje": 0.64,
    "Corrector": 1.59,
    "Cortadora circular": 2.33,
    "Cortadora de papel": 3.81,
    "Escarcha / Brillantina": 0.40,
    "Fomix (Paquete)": 0.85,
    "Fomix (Pliego)": 1.10,
    "Fomix Escarchado (Pliego)": 1.20,
    "Fomix Escharchado(Paquete)": 0.90,
    "Goma líquida (Uso estimado)": 0.30,
    "Ojitos locos (Par)": 0.15,
    "Silicona en barra(paquete)": 0.77,
    "Tijeras (Uso proporcional)": 0.60
}

# Función para cargar el inventario guardado
def cargar_inventario():
    if os.path.exists(ARCHIVO_INVENTARIO):
        try:
            with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return inventario_base
    return inventario_base

# Función para guardar de forma permanente y ordenar alfabéticamente
def guardar_inventario(inventario):
    # Ordenamos alfabéticamente antes de guardar
    inventario_ordenado = dict(sorted(inventario.items()))
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as f:
        json.dump(inventario_ordenado, f, ensure_ascii=False, indent=4)
    return inventario_ordenado

# Inicializar el inventario real leyendo desde el archivo permanente
if "inventario" not in st.session_state:
    st.session_state.inventario = cargar_inventario()

# Inicializar la lista de compras del usuario
if "compras" not in st.session_state:
    st.session_state.compras = []


# --- SECCIÓN A: AGREGAR NUEVOS MATERIALES AL INVENTARIO ---
with st.expander("➕ Agregar nuevo material a la lista de precios (Inventario)"):
    nuevo_nombre = st.text_input("Nombre del nuevo material (ej. Encaje, Caja de cartón):").strip()
    nuevo_precio = st.number_input("Precio por unidad ($):", min_value=0.0, step=0.05, format="%.2f")
    
    if st.button("Guardar material nuevo"):
        if nuevo_nombre:
            # Añadir al estado actual
            st.session_state.inventario[nuevo_nombre] = nuevo_precio
            # GUARDADO PERMANENTE: Escribir en el archivo
            st.session_state.inventario = guardar_inventario(st.session_state.inventario)
            
            st.success(f"¡Guardado permanentemente! Ahora puedes seleccionar '{nuevo_nombre}' en la lista de abajo.")
            st.rerun()
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
