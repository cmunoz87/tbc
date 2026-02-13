import streamlit as st

st.set_page_config(page_title="Solicitud TBC")

st.title("SOLICITUD DE EXAMENES TUBERCULOSIS")

# -------- FUNCION REFRESCAR --------
def refrescar():
    st.session_state.clear()
    st.rerun()

# -------- EDAD --------
edad = st.number_input(
    "EDAD DEL PACIENTE",
    min_value=0,
    max_value=120,
    value=None,
    placeholder="Ingrese edad"
)

menor_15 = edad is not None and edad < 15

# -------- MOTIVO --------
motivo = st.selectbox(
    "MOTIVO DEL ESTUDIO",
    [
        None,
        "PESQUISA DE CASO PRESUNTIVO DE TUBERCULOSIS (CPT)",
        "PERSISTENCIA DE SINTOMAS (CPT CON EXAMEN NEGATIVO)",
        "SOSPECHA CLINICA (SIN CRITERIO DE CPT)",
        "SOSPECHA DE MICOBACTERIA NO TUBERCULOSA (MNT)",
        "CONTROL DE TRATAMIENTO"
    ],
    index=0
)

# -------- ANTECEDENTES --------
def antecedentes_tratamiento():
    return st.radio(
        "ANTECEDENTES DE TRATAMIENTO",
        [
            "CASO NUEVO (SIN TRATAMIENTO PREVIO)",
            "SOSPECHA DE FRACASO DE TRATAMIENTO",
            "PREVIAMENTE TRATADO RECAIDA",
            "PREVIAMENTE TRATADO PERDIDA DE SEGUIMIENTO"
        ],
        index=None
    )

# -------- GRUPOS VULNERABLES --------
def grupos_vulnerables():
    seleccion = st.multiselect(
        "GRUPOS VULNERABLES",
        [
            "DIABETES",
            "EXTRANJERO",
            "INMUNOSUPRESION (ESPECIFICAR)",
            "MAYOR DE 65 AÑOS",
            "PERSONAL DE SALUD",
            "PERSONA PRIVADA DE LIBERTAD",
            "PUEBLO INDIGENA",
            "SITUACION DE CALLE",
            "TRABAJADOR EXPUESTO A SILICE",
            "OTRAS POBLACIONES CERRADAS (ESPECIFICAR)",
            "OTROS GRUPOS (ESPECIFICAR)",
            "ALCOHOL/DROGAS",
            "PV VIH",
            "CONTACTO TBC SENSIBLE",
            "CONTACTO TBC RESISTENTE",
            "MENOR DE 15 AÑOS"
        ]
    )

    if "INMUNOSUPRESION (ESPECIFICAR)" in seleccion:
        st.text_input("ESPECIFICAR INMUNOSUPRESION")

    if "OTRAS POBLACIONES CERRADAS (ESPECIFICAR)" in seleccion:
        st.text_input("ESPECIFICAR POBLACION CERRADA")

    if "OTROS GRUPOS (ESPECIFICAR)" in seleccion:
        st.text_input("ESPECIFICAR OTRO GRUPO")

    return seleccion

# -------- SINTOMAS --------
def sintomas():
    st.multiselect(
        "SINTOMAS",
        ["TOS", "FIEBRE", "BAJA DE PESO", "SUDORACION NOCTURNA", "HEMOPTISIS"]
    )

# -------- LOGICA --------
examenes = []

if motivo:

    # ======================================================
    # CPT
    # ======================================================
    if motivo == "PESQUISA DE CASO PRESUNTIVO DE TUBERCULOSIS (CPT)":

        antecedentes_tratamiento()

        muestra = st.selectbox(
            "TIPO DE MUESTRA",
            [
                None,
                "ESPUTO",
                "TEJIDO OSEO",
                "TEJIDO PLEURAL",
                "DEPOSICION",
                "CONTENIDO GASTRICO",
                "LAVADO BROCO ALVEOLAR",
                "LIQUIDO CEFALORRAQUIDEO",
                "LIQUIDO PLEURAL",
                "OTROS LIQUIDOS TEJIDOS O SANGRE (ESPECIFICAR)",
                "TEJIDO GANGLIONAR",
                "ASPIRADO BRONQUIAL",
                "ORINA"
            ],
            index=0
        )

        if muestra == "ESPUTO":

            st.radio("ESPECIFICAR 1 O 2 MUESTRAS", ["1 MUESTRA", "2 MUESTRAS"], index=None)

            grupos = grupos_vulnerables()
            sintomas()

            examenes.append("PCR MYCOBACTERIUM TUBERCULOSIS - MTB/RIF")

            if (
                "PV VIH" in grupos
                or "CONTACTO TBC SENSIBLE" in grupos
                or "CONTACTO TBC RESISTENTE" in grupos
                or menor_15
            ):
                examenes.append("CULTIVO KOCH")

        elif muestra in ["TEJIDO OSEO", "TEJIDO PLEURAL", "DEPOSICION"]:
            examenes.append("PCR MYCOBACTERIUM TUBERCULOSIS - MTB/RIF")

        elif muestra:

            if muestra == "ORINA":
                st.radio(
                    "ESPECIFICAR SI 1RA, 2DA O 3RA MUESTRA",
                    ["1RA MUESTRA", "2DA MUESTRA", "3RA MUESTRA"],
                    index=None
                )

            if muestra == "OTROS LIQUIDOS TEJIDOS O SANGRE (ESPECIFICAR)":
                st.text_input("ESPECIFICAR")

            examenes = [
                "PCR MYCOBACTERIUM TUBERCULOSIS - MTB/RIF",
                "CULTIVO KOCH"
            ]

    # ======================================================
    # PERSISTENCIA SINTOMAS
    # ======================================================
    elif motivo == "PERSISTENCIA DE SINTOMAS (CPT CON EXAMEN NEGATIVO)":

        st.info("TIPO DE MUESTRA: ESPUTO")

        st.radio("ESPECIFICAR 1 O 2 MUESTRAS", ["1 MUESTRA", "2 MUESTRAS"], index=None)

        antecedentes_tratamiento()
        sintomas()

        examenes = [
            "PCR MYCOBACTERIUM TUBERCULOSIS - MTB/RIF",
            "CULTIVO KOCH"
        ]

    # ======================================================
    # SOSPECHA CLINICA
    # ======================================================
    elif motivo == "SOSPECHA CLINICA (SIN CRITERIO DE CPT)":

        st.info("TIPO DE MUESTRA: ESPUTO")

        st.radio("ESPECIFICAR 1 O 2 MUESTRAS", ["1 MUESTRA", "2 MUESTRAS"], index=None)

        antecedentes_tratamiento()

        examenes = [
            "PCR MYCOBACTERIUM TUBERCULOSIS - MTB/RIF",
            "CULTIVO KOCH"
        ]

    # ======================================================
    # SOSPECHA MNT
    # ======================================================
    elif motivo == "SOSPECHA DE MICOBACTERIA NO TUBERCULOSA (MNT)":

        st.info("TIPO DE MUESTRA: ORINA")

        antecedentes_tratamiento()
        grupos_vulnerables()
        sintomas()

        examenes = ["PCR", "CULTIVO"]

    # ======================================================
    # CONTROL TRATAMIENTO
    # ======================================================
    elif motivo == "CONTROL DE TRATAMIENTO":

        muestra = st.selectbox(
            "TIPO DE MUESTRA",
            [None, "ESPUTO", "ORINA"],
            index=0
        )

        if muestra == "ESPUTO":

            st.selectbox(
                "MES DE TRATAMIENTO",
                [None] + list(range(1, 11)),
                index=0
            )

            examenes = ["BACILOSCOPIA", "CULTIVO KOCH"]

        elif muestra == "ORINA":
            examenes = ["CULTIVO KOCH"]

# -------- RESULTADO --------
if examenes:
    st.subheader("EXAMENES A REALIZAR")
    for e in set(examenes):
        st.write("✔", e)

# -------- BOTON REFRESCAR --------
st.divider()
st.button("REFRESCAR FORMULARIO", on_click=refrescar)
