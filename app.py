import streamlit as st

st.set_page_config(page_title="Simulación TBC", layout="centered")

# ----------------------------
# Utilidades
# ----------------------------
def reset_app():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def select_with_placeholder(label: str, options: list[str], key: str):
    opts = ["-- Seleccione --"] + options
    return st.selectbox(label, opts, index=0, key=key)

# ----------------------------
# Estado para resultados
# ----------------------------
if "show_results" not in st.session_state:
    st.session_state["show_results"] = False
if "examenes_out" not in st.session_state:
    st.session_state["examenes_out"] = []

# ----------------------------
# UI
# ----------------------------
st.title("Simulación de Solicitud de Investigación Bacteriológica de Tuberculosis")

st.subheader("Datos del paciente")
edad = st.number_input(
    "Edad del paciente (años)",
    min_value=0,
    max_value=120,
    value=0,
    step=1,
    key="edad_paciente",
)

st.divider()

escenarios = [
    "Pesquisa de Caso Presuntivo de Tuberculosis (CPT)",
    "Persistencia de síntomas (CPT con examen negativo)",
    "Sospecha clínica (sin criterio de CPT)",
    "Sospecha de Micobacteria No Tuberculosa (MNT)",
    "Control de tratamiento",
]
escenario = select_with_placeholder("Escenario clínico (obligatorio)", escenarios, key="escenario")

st.divider()

# ----------------------------
# Catálogos
# ----------------------------
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
# Variables de formulario
# ----------------------------
muestra = None
antecedentes = None
grupo_vulnerable = []
sintomas = []
mes_tratamiento = None

is_complete = False
validation_errors = []

# ----------------------------
# Formulario por escenario
# ----------------------------
if escenario == "-- Seleccione --":
    is_complete = False

elif escenario == "Pesquisa de Caso Presuntivo de Tuberculosis (CPT)":
    muestra = select_with_placeholder("Tipo de muestra (obligatorio, 1 sola)", muestras_cpt, key="muestra_cpt")
    if muestra == "-- Seleccione --":
        validation_errors.append("Debe seleccionar el tipo de muestra.")

    if muestra == "Esputo":
        n_esputo = select_with_placeholder(
            "Cantidad de muestras de esputo (obligatorio)",
            ["1 muestra", "2 muestras"],
            key="n_esputo",
        )
        if n_esputo == "-- Seleccione --":
            validation_errors.append("Debe indicar 1 o 2 muestras de esputo.")

    antecedentes = select_with_placeholder(
        "Antecedentes de tratamiento (obligatorio, 1 sola)",
        antecedentes_opts,
        key="ant_cpt",
    )
    if antecedentes == "-- Seleccione --":
        validation_errors.append("Debe seleccionar antecedentes de tratamiento.")

    st.subheader("Grupo vulnerable (puede seleccionar más de 1)")
    grupo_vulnerable = st.multiselect("Seleccione", grupo_vulnerable_opts, default=[], key="gv_cpt")

    # Mostrar "Especificar" SOLO si se selecciona
    if "Inmunosupresión (ESPECIFICAR)" in grupo_vulnerable:
        txt_inmuno = st.text_input("Especificar inmunosupresión", key="esp_inmuno")
        if not txt_inmuno.strip():
            validation_errors.append("Debe especificar inmunosupresión.")

    if "Otras poblaciones cerradas (ESPECIFICAR)" in grupo_vulnerable:
        txt_pob = st.text_input("Especificar otras poblaciones cerradas", key="esp_poblaciones")
        if not txt_pob.strip():
            validation_errors.append("Debe especificar otras poblaciones cerradas.")

    if "Otros grupos (ESPECIFICAR)" in grupo_vulnerable:
        txt_otros = st.text_input("Especificar otros grupos", key="esp_otros_grupos")
        if not txt_otros.strip():
            validation_errors.append("Debe especificar otros grupos.")

    st.subheader("Síntomas (puede seleccionar más de 1)")
    sintomas = st.multiselect("Seleccione", sintomas_opts, default=[], key="sint_cpt")

    is_complete = len(validation_errors) == 0

elif escenario == "Persistencia de síntomas (CPT con examen negativo)":
    muestra = select_with_placeholder("Tipo de muestra (obligatorio, 1 sola)", muestras_amplias, key="muestra_persist")
    if muestra == "-- Seleccione --":
        validation_errors.append("Debe seleccionar el tipo de muestra.")

    if muestra == "Otras muestras (ESPECIFICAR)":
        txt_m = st.text_input("Especificar muestra", key="esp_muestra_persist")
        if not txt_m.strip():
            validation_errors.append("Debe especificar la muestra.")

    antecedentes = select_with_placeholder(
        "Antecedentes de tratamiento (obligatorio, 1 sola)",
        antecedentes_opts,
        key="ant_persist",
    )
    if antecedentes == "-- Seleccione --":
        validation_errors.append("Debe seleccionar antecedentes de tratamiento.")

    is_complete = len(validation_errors) == 0

elif escenario == "Sospecha clínica (sin criterio de CPT)":
    muestra = select_with_placeholder("Tipo de muestra (obligatorio, 1 sola)", muestras_amplias, key="muestra_sospecha")
    if muestra == "-- Seleccione --":
        validation_errors.append("Debe seleccionar el tipo de muestra.")

    if muestra == "Otras muestras (ESPECIFICAR)":
        txt_m = st.text_input("Especificar muestra", key="esp_muestra_sospecha")
        if not txt_m.strip():
            validation_errors.append("Debe especificar la muestra.")

    antecedentes = select_with_placeholder(
        "Antecedentes de tratamiento (obligatorio, 1 sola)",
        antecedentes_opts,
        key="ant_sospecha",
    )
    if antecedentes == "-- Seleccione --":
        validation_errors.append("Debe seleccionar antecedentes de tratamiento.")

    is_complete = len(validation_errors) == 0

elif escenario == "Sospecha de Micobacteria No Tuberculosa (MNT)":
    muestra = select_with_placeholder("Tipo de muestra (obligatorio, 1 sola)", muestras_amplias, key="muestra_mnt")
    if muestra == "-- Seleccione --":
        validation_errors.append("Debe seleccionar el tipo de muestra.")

    if muestra == "Otras muestras (ESPECIFICAR)":
        txt_m = st.text_input("Especificar muestra", key="esp_muestra_mnt")
        if not txt_m.strip():
            validation_errors.append("Debe especificar la muestra.")

    antecedentes = select_with_placeholder(
        "Antecedentes de tratamiento (obligatorio, 1 sola)",
        antecedentes_opts,
        key="ant_mnt",
    )
    if antecedentes == "-- Seleccione --":
        validation_errors.append("Debe seleccionar antecedentes de tratamiento.")

    st.subheader("Grupo vulnerable (puede seleccionar más de 1)")
    grupo_vulnerable = st.multiselect("Seleccione", grupo_vulnerable_opts, default=[], key="gv_mnt")

    if "Inmunosupresión (ESPECIFICAR)" in grupo_vulnerable:
        txt_inmuno = st.text_input("Especificar inmunosupresión", key="esp_inmuno_mnt")
        if not txt_inmuno.strip():
            validation_errors.append("Debe especificar inmunosupresión.")

    if "Otras poblaciones cerradas (ESPECIFICAR)" in grupo_vulnerable:
        txt_pob = st.text_input("Especificar otras poblaciones cerradas", key="esp_poblaciones_mnt")
        if not txt_pob.strip():
            validation_errors.append("Debe especificar otras poblaciones cerradas.")

    if "Otros grupos (ESPECIFICAR)" in grupo_vulnerable:
        txt_otros = st.text_input("Especificar otros grupos", key="esp_otros_grupos_mnt")
        if not txt_otros.strip():
            validation_errors.append("Debe especificar otros grupos.")

    st.subheader("Síntomas (puede seleccionar más de 1)")
    sintomas = st.multiselect("Seleccione", sintomas_opts, default=[], key="sint_mnt")

    is_complete = len(validation_errors) == 0

elif escenario == "Control de tratamiento":
    muestra = select_with_placeholder("Tipo de muestra (obligatorio, 1 sola)", ["Esputo", "Orina"], key="muestra_ctrl")
    if muestra == "-- Seleccione --":
        validation_errors.append("Debe seleccionar el tipo de muestra.")

    mes_opts = [str(i) for i in range(1, 11)] + ["6 meses post alta"]
    mes_tratamiento = select_with_placeholder("Mes de tratamiento (obligatorio)", mes_opts, key="mes_ctrl")
    if mes_tratamiento == "-- Seleccione --":
        validation_errors.append("Debe seleccionar el mes de tratamiento.")

    if muestra == "Orina" and mes_tratamiento not in ("-- Seleccione --", "4"):
        validation_errors.append("Para ORINA, corresponde solo el mes 4.")

    is_complete = len(validation_errors) == 0

# ----------------------------
# Botón para calcular exámenes (solo cuando todo esté completo)
# ----------------------------
st.divider()
calcular = st.button("Calcular exámenes", type="primary")

if calcular:
    st.session_state["show_results"] = False
    st.session_state["examenes_out"] = []

    if not is_complete:
        st.error("Faltan campos obligatorios por completar.")
        for msg in validation_errors:
            st.write(f"- {msg}")
    else:
        examenes = []

        if escenario == "Pesquisa de Caso Presuntivo de Tuberculosis (CPT)":
            examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF"]
            gatilla_cultivo = False

            if int(edad) < 15:
                gatilla_cultivo = True

            if any(x in grupo_vulnerable for x in ["PV VIH", "Contacto TB-sensible", "Contacto TB-resistente"]):
                gatilla_cultivo = True

            if gatilla_cultivo:
                examenes.append("Cultivo Koch")

        elif escenario in [
            "Persistencia de síntomas (CPT con examen negativo)",
            "Sospecha clínica (sin criterio de CPT)",
            "Sospecha de Micobacteria No Tuberculosa (MNT)",
        ]:
            examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF", "Cultivo Koch"]
            if muestra in ["Tejido óseo", "Tejido pulmonar", "Deposición"]:
                examenes = ["PCR Mycobacterium tuberculosis – MTB/RIF"]

        elif escenario == "Control de tratamiento":
            if muestra == "Esputo":
                examenes = ["Baciloscopía", "Cultivo Koch"]
            else:
                examenes = ["Cultivo Koch"]

        st.session_state["examenes_out"] = examenes
        st.session_state["show_results"] = True

# ----------------------------
# Mostrar resultados SOLO cuando se calculó y está completo
# ----------------------------
if st.session_state["show_results"]:
    st.subheader("Exámenes a realizar")
    for e in st.session_state["examenes_out"]:
        st.write(f"- {e}")

st.divider()

if st.button("Nuevo caso (borrar y simular otro)"):
    reset_app()

st.markdown("---")
st.write("Elaborado por TM Camilo Muñoz, Febrero 2026")
