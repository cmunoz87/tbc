import streamlit as st

st.set_page_config(page_title="Solicitud Micobacterias")

st.title("🧪 Solicitud Exámenes Micobacterias")

# -----------------------------
# Edad paciente
# -----------------------------
edad = st.number_input("Edad del paciente", min_value=0, max_value=120, step=1)
menor_15 = edad < 15

# -----------------------------
# Motivo estudio
# -----------------------------
motivo = st.selectbox(
    "Motivo del estudio",
    [
        "CPT",
        "Persistencia de síntomas",
        "Sospecha clínica sin CPT",
        "Sospecha MNT",
        "Control de tratamiento"
    ]
)

examenes = []

# -----------------------------
# FUNCIONES APOYO
# -----------------------------
def antecedentes_tratamiento():
    return st.radio(
        "Antecedentes de tratamiento",
        [
            "Caso nuevo",
            "Fracaso tratamiento",
            "Recaída",
            "Pérdida seguimiento"
        ]
    )

def sintomas():
    return st.multiselect(
        "Síntomas",
        ["Tos", "Fiebre", "Baja peso", "Sudoración nocturna", "Hemoptisis"]
    )

def grupos_vulnerables():
    return st.multiselect(
        "Grupos vulnerables",
        [
            "Diabetes",
            "Extranjero",
            "Inmunosupresión",
            "Mayor 65",
            "Personal salud",
            "Privado libertad",
            "Pueblo indígena",
            "Situación calle",
            "Silicosis",
            "Alcohol/Drogas",
            "PV VIH",
            "Contacto TBC sensible",
            "Contacto TBC resistente"
        ]
    )

# -----------------------------
# CPT
# -----------------------------
if motivo == "CPT":

    antecedentes_tratamiento()

    muestra = st.selectbox(
        "Tipo muestra",
        [
            "Esputo",
            "Tejido óseo",
            "Tejido pleural",
            "Deposición",
            "Contenido gástrico",
            "Lavado broncoalveolar",
            "LCR",
            "Líquido pleural",
            "Tejido ganglionar",
            "Aspirado bronquial",
            "Orina",
            "Otros líquidos/tejidos/sangre"
        ]
    )

    if muestra == "Esputo":

        st.radio("Número muestras", ["1", "2"])
        grupos = grupos_vulnerables()
        sintomas()

        examenes.append("PCR MTB/RIF")

        if (
            "PV VIH" in grupos or
            "Contacto TBC sensible" in grupos or
            "Contacto TBC resistente" in grupos or
            menor_15
        ):
            examenes.append("Cultivo Koch")

    elif muestra in ["Tejido óseo", "Tejido pleural", "Deposición"]:
        examenes.append("PCR MTB/RIF")

    else:

        if muestra == "Orina":
            st.radio("Número muestra orina", ["1ra", "2da", "3ra"])

        if muestra == "Otros líquidos/tejidos/sangre":
            st.text_input("Especificar tipo muestra")

        examenes.append("PCR MTB/RIF")
        examenes.append("Cultivo Koch")

# -----------------------------
# Persistencia síntomas
# -----------------------------
elif motivo == "Persistencia de síntomas":

    st.radio("Número muestras esputo", ["1", "2"])
    antecedentes_tratamiento()
    sintomas()

    examenes = ["PCR MTB/RIF", "Cultivo Koch"]

# -----------------------------
# Sospecha clínica sin CPT
# -----------------------------
elif motivo == "Sospecha clínica sin CPT":

    st.radio("Número muestras esputo", ["1", "2"])
    antecedentes_tratamiento()

    examenes = ["PCR MTB/RIF", "Cultivo Koch"]

# -----------------------------
# Sospecha MNT
# -----------------------------
elif motivo == "Sospecha MNT":

    muestra = st.selectbox("Tipo muestra", ["Orina"])

    antecedentes_tratamiento()
    grupos_vulnerables()
    sintomas()

    examenes = ["PCR", "Cultivo"]

# -----------------------------
# Control tratamiento
# -----------------------------
elif motivo == "Control de tratamiento":

    muestra = st.selectbox("Tipo muestra", ["Esputo", "Orina"])

    if muestra == "Esputo":
        st.selectbox("Mes tratamiento", list(range(1, 11)))
        examenes = ["Baciloscopía", "Cultivo"]

    else:
        examenes = ["Cultivo"]

# -----------------------------
# RESULTADO FINAL
# -----------------------------
st.subheader("Exámenes a realizar")

if examenes:
    for ex in set(examenes):
        st.write("✔", ex)