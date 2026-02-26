import streamlit as st

st.set_page_config(page_title="Simulación TBC", layout="centered")

# ----------------------------
# Utilidades
# ----------------------------
def reset_app():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def requiere_especificar(opcion: str) -> bool:
    return "(ESPECIFICAR)" in opcion.upper() or "OTRAS MUESTRAS" in opcion.upper()

# ----------------------------
# UI
# ----------------------------
st.title("Simulación de Solicitud de Investigación Bacteriológica de Tuberculosis")

st.write("Seleccione un escenario clínico y complete los campos requeridos. Los exámenes se agregan según la lógica definida.")

escenarios = [
    "1) Pesquisa de Caso Presuntivo de Tuberculosis (CPT)",
    "2) Persistencia de síntomas (CPT con examen negativo)",
    "3) Sospecha clínica (sin criterio de CPT)",
    "4) Sospecha de Micobacteria No Tuberculosa (MNT)",
    "5) Control de tratamiento",
]
escenario = st.selectbox("Escenario clínico (obligatorio)", escenarios, key="escenario")

st.divider()

# Campos comunes en varios escenarios
edad = None
antecedentes = None
grupo_vulnerable = []
sintomas = []

antecedentes_opts = [
    "Caso nuevo (sin tratamiento previo)",
    "Sospecha de fracaso de tratamiento",
    "Previamente tratado – recaída",
    "Previamente tratado – pérdida de seguimiento",
]

sintomas_opts = [
    "Baja de peso",
    "Sudoración nocturna",
    "Esputo con sangre",
    "Fiebre",
]

grupo_vulnerable_opts = [
    "Diabetes",
    "Extranjero",
    "Inmunosupresión (ESPECIFICAR)",
    "Mayor de 65 años",
    "Personal de salud",
    "Persona privada de libertad",
    "Pueblo indígena",
    "Situación de calle",
    "Trabajador expuesto a sílice",
    "Otras poblaciones cerradas (ESPECIFICAR)",
    "Otros grupos (ESPECIFICAR)",
    "Alcohol/drogas",
    "PV VIH",
    "Contacto TB-sensible",
    "Contacto TB-resistente",
]

# Listas de muestras
muestras_cpt = ["Esputo", "Aspirado endotraqueal", "Secreción bronquial"]

muestras_amplias = [
    "Contenido gástrico",
    "Lavado broncoalveolar",
    "Líquido cefalorraquídeo",
    "Líquido pleural",
    "Tejido ganglionar",
    "Aspirado bronquial",
    "Otras muestras (ESPECIFICAR)",
    "Orina",
    "Tejido óseo",
    "Tejido pleural",
    "Tejido pulmonar",
    "Deposición",
]

# ----------------------------
# Lógica por escenario
# ----------------------------
examenes = []
observaciones = []
muestra = None

if escenario.startswith("1)"):
    col1, col2 = st.columns([1, 1])

    with col1:
        muestra = st.radio("Tipo de muestra (1 sola)", muestras_cpt, key="muestra_cpt")

    with col2:
        edad = st.number_input("Edad (años)", min_value=0, max_value=120, value=0, step=1, key="edad_cpt")

    if muestra == "Esputo":
        st.radio("Cantidad de muestras de esputo", ["1 muestra", "2 muestras"], key="n_esputo")

    antecedentes = st.radio("Antecedentes de tratamiento (1 sola)", antecedentes_opts, key="ant_cpt")

    st.subheader("Grupo vulnerable (puede seleccionar más de 1)")
    grupo_vulnerable = st.multiselect("Seleccione", grupo_vulnerable_opts, default=[], key="gv_cpt")

    # Campos "ESPECIFICAR" en grupo vulnerable
    if "Inmunosupresión (ESPECIFICAR)" in grupo_vulnerable:
        st.text_input("Especificar inmunosupresión", key="esp_inmuno")
    if "Otras poblaciones cerradas (ESPECIFICAR)" in grupo_vulnerable:
        st.text_input("Especificar otras poblaciones cerradas", key="esp_poblaciones")
    if "Otros grupos (ESPECIFICAR)" in grupo_vulnerable:
        st.text_input("Especificar otros grupos", key="esp_otros_grupos")

    st.subheader("Síntomas (puede seleccionar más de 1)")
    sintomas = st.multiselect("Seleccione", sintomas_opts, default=[], key="sint_cpt")

    # Exámenes
    examenes.append("PCR Mycobacterium tuberculosis – MTB/RIF")

    # Regla de cultivo en CPT
    gatilla_cultivo = False
    if edad is not None and int(edad) < 15:
        gatilla_cultivo = True
        observaciones.append("Se agrega Cultivo (menor de 15 años).")

    if any(x in grupo_vulnerable for x in ["PV VIH", "Contacto TB-sensible", "Contacto TB-resistente"]):
        gatilla_cultivo = True
        observaciones.append("Se agrega Cultivo (criterio en Grupo vulnerable).")

    if gatilla_cultivo:
        examenes.append("Cultivo Koch")

elif escenario.startswith("2)"):
    muestra = st.selectbox("Tipo de muestra (1 sola)", muestras_amplias, key="muestra_persist")
    if requiere_especificar(muestra):
        st.text_input("Especificar muestra", key="esp_muestra_persist")

    antecedentes = st.radio("Antecedentes de tratamiento (1 sola)", antecedentes_opts, key="ant_persist")

    # Exámenes por defecto
    examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF", "Cultivo Koch"]

    # Excepción
    if muestra in ["Tejido óseo", "Tejido pulmonar", "Deposición"]:
        examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF"]
        observaciones.append("Regla: en tejido óseo, tejido pulmonar o deposición se realiza solo PCR (sin cultivo).")

elif escenario.startswith("3)"):
    muestra = st.selectbox("Tipo de muestra (1 sola)", muestras_amplias, key="muestra_sospecha")
    if requiere_especificar(muestra):
        st.text_input("Especificar muestra", key="esp_muestra_sospecha")

    antecedentes = st.radio("Antecedentes de tratamiento (1 sola)", antecedentes_opts, key="ant_sospecha")

    examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF", "Cultivo Koch"]

    if muestra in ["Tejido óseo", "Tejido pulmonar", "Deposición"]:
        examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF"]
        observaciones.append("Regla: en tejido óseo, tejido pulmonar o deposición se realiza solo PCR (sin cultivo).")

elif escenario.startswith("4)"):
    muestra = st.selectbox("Tipo de muestra (1 sola)", muestras_amplias, key="muestra_mnt")
    if requiere_especificar(muestra):
        st.text_input("Especificar muestra", key="esp_muestra_mnt")

    antecedentes = st.radio("Antecedentes de tratamiento (1 sola)", antecedentes_opts, key="ant_mnt")

    st.subheader("Grupo vulnerable (puede seleccionar más de 1)")
    grupo_vulnerable = st.multiselect("Seleccione", grupo_vulnerable_opts, default=[], key="gv_mnt")

    if "Inmunosupresión (ESPECIFICAR)" in grupo_vulnerable:
        st.text_input("Especificar inmunosupresión", key="esp_inmuno_mnt")
    if "Otras poblaciones cerradas (ESPECIFICAR)" in grupo_vulnerable:
        st.text_input("Especificar otras poblaciones cerradas", key="esp_poblaciones_mnt")
    if "Otros grupos (ESPECIFICAR)" in grupo_vulnerable:
        st.text_input("Especificar otros grupos", key="esp_otros_grupos_mnt")

    st.subheader("Síntomas (puede seleccionar más de 1)")
    sintomas = st.multiselect("Seleccione", sintomas_opts, default=[], key="sint_mnt")

    examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF", "Cultivo Koch"]

    if muestra in ["Tejido óseo", "Tejido pulmonar", "Deposición"]:
        examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF"]
        observaciones.append("Regla: en tejido óseo, tejido pulmonar o deposición se realiza solo PCR (sin cultivo).")

elif escenario.startswith("5)"):
    muestra = st.radio("Tipo de muestra (1 sola)", ["Esputo", "Orina"], key="muestra_ctrl")

    mes_opts = [str(i) for i in range(1, 11)] + ["6 meses post alta"]
    mes = st.selectbox("Mes de tratamiento", mes_opts, key="mes_ctrl")

    if muestra == "Esputo":
        st.info("Esputo: 1 muestra.")
        examenes = ["Baciloscopía", "Cultivo Koch"]
    else:
        st.info("Orina: 1 muestra. Solo aplica en mes 4.")
        if mes != "4":
            st.warning("Para ORINA, la solicitud corresponde solo al mes 4. Ajuste el mes o cambie a esputo.")
        examenes = ["Cultivo Koch"]

# ----------------------------
# Resumen
# ----------------------------
st.divider()
st.subheader("Resumen del caso")

st.write(f"Escenario: {escenario}")
if muestra is not None:
    st.write(f"Muestra: {muestra}")

if escenario.startswith("1)") and "n_esputo" in st.session_state:
    st.write(f"Cantidad de esputo: {st.session_state.get('n_esputo')}")

if escenario.startswith("5)"):
    st.write(f"Mes de tratamiento: {st.session_state.get('mes_ctrl')}")

if antecedentes is not None:
    st.write(f"Antecedentes de tratamiento: {antecedentes}")

if escenario.startswith("1)") or escenario.startswith("4)"):
    st.write(f"Grupo vulnerable: {', '.join(grupo_vulnerable) if grupo_vulnerable else 'Ninguno'}")
    st.write(f"Síntomas: {', '.join(sintomas) if sintomas else 'Ninguno'}")

st.markdown("**Exámenes a realizar:**")
for e in examenes:
    st.write(f"- {e}")

if observaciones:
    st.markdown("**Observaciones / reglas aplicadas:**")
    for o in observaciones:
        st.write(f"- {o}")

st.divider()

# Botón de "refresh" (nuevo caso)
if st.button("Nuevo caso (borrar y simular otro)", type="primary"):
    reset_app()

st.markdown("---")
st.write("Elaborado por TM Camilo Muñoz, Febrero 2026")
