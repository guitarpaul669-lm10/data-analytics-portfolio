import streamlit as st
import random



st.set_page_config(page_title="Big Five App", layout="centered")

# Seiten-Navigation
seite = st.sidebar.radio("Navigation", ["Fragebogen", "Auswertung", "Berufsempfehlung"])

fragen = [
    ("Ich arbeite gründlich", "Gewissenhaftigkeit"),
    ("Ich bin kommunikativ", "Extraversion"),
    ("Ich bin manchmal grob zu anderen", "Verträglichkeit"),  # negativ gepolt
    ("Ich bin originell", "Offenheit"),
    ("Ich mache mir oft Sorgen", "Neurotizismus"),
    ("Ich kann verzeihen", "Verträglichkeit"),
    ("Ich bin eher faul", "Gewissenhaftigkeit"),  # negativ gepolt
    ("Ich bin gesellig", "Extraversion"),
    ("Ich schätze künstlerische Erfahrungen", "Offenheit"),
    ("Ich werde leicht nervös", "Neurotizismus"),
    ("Ich erledige Aufgaben wirksam und effizient", "Gewissenhaftigkeit"),
    ("Ich bin zurückhaltend", "Extraversion"),  # negativ gepolt
    ("Ich bin freundlich im Umgang mit anderen", "Verträglichkeit"),
    ("Ich habe lebhafte Fantasien", "Offenheit"),
    ("Ich kann gut mit Stress umgehen", "Neurotizismus"), #negativ gepolt
    ("Ich bin wissbegierig", "Offenheit")
]

negativ_gepolte = [
    "Ich bin manchmal grob zu anderen",
    "Ich bin eher faul",
    "Ich bin zurückhaltend",
    "Ich kann gut mit Stress umgehen"
]

if "antworten" not in st.session_state:
    st.session_state.antworten = {}

if seite == "Fragebogen":

    st.title("Persönlichkeitsmodell der Job Satisfaction für Berufsgruppen")
    st.markdown("In diesem Programm ...")
    st.divider()
    st.header("Personangaben")
    with st.form(key="person_info"):
        name = st.text_input("Geben Sie ihren Namen ein:")
        alter = st.number_input("Geben Sie ihr Alter ein: ", min_value=16, max_value=120)
        geschlecht = st.radio("Geschlecht:", options=["Männlich", "Weiblich", "Divers"], index=None)

        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            if not name or not geschlecht:
                st.warning("Bitte geben Sie die überliegenden Daten ein.")
            else: 
                st.success("Angaben gespeichert")
                st.session_state["Name"] = name
                st.session_state["Alter"] = alter
                st.session_state["Geschlecht"] = geschlecht
                
    st.divider()
    st.header("Fragen zu den Big Five")
    st.markdown("Die folgenden Fragen beziehen sich auf die 5 Persönlichkeitsfaktoren (Big Five).")
    st.markdown(" Die 5 Facetten sind:")
    st.markdown("""
    * Extraversion
    * Neurotizismus
    * Offenheit
    * Gewissenhaftigkeit
    * Verträglichkeit
    """)
    st.divider()
    with st.form(key="fragebogen_form"):
        st.markdown("Die Fragen sind immer nach diesem Muster strukturiert:")
        st.markdown("**1** = Stimme überhaupt nicht zu &nbsp;&nbsp;&nbsp; ... &nbsp;&nbsp;&nbsp; **7** = Stimme völlig zu")
        st.markdown("Bitte wählen Sie die entsprechende Antwortmöglichkeiten an.")

        antworten_temp = {}
        

        for i, (frage, dimension) in enumerate(fragen):
            antwort = st.radio(
                frage,
                options=[1, 2, 3, 4, 5, 6, 7],
                format_func=lambda x: {
                    1: "Stimme überhaupt nicht zu",
                    2: "Stimme nicht zu",
                    3: "Stimme eher nicht zu",
                    4: "Neutral",
                    5: "Stimme eher zu",
                    6: "Stimme zu",
                    7: "Stimme völlig zu"
                }[x],
                key=f"frage_{i}",
                index=None
            )

            if antwort is not None:
                if frage in negativ_gepolte:
                    antwort = 8 - antwort  # Hier wird korrekt invertiert

                if dimension not in antworten_temp:
                    antworten_temp[dimension] = []
                antworten_temp[dimension].append(antwort)

        auswerten_button = st.form_submit_button(label="Auswertung starten")
        if auswerten_button:
            st.session_state.antworten = antworten_temp
            st.success("Antworten gespeichert. Wechseln Sie zur Auswertung.")

elif seite == "Auswertung":
    st.title("Auswertung Ihrer Big Five Merkmale")
    st.markdown("In dieser Übersicht bedeudet 1 = wenig ausgeprägt & 7 = sehr ausgeprägt")

    if not st.session_state.get("antworten"):
        st.warning("Bitte füllen Sie zuerst den Fragebogen aus.")
    else:
        for dimension in ["Extraversion", "Neurotizismus", "Offenheit", "Gewissenhaftigkeit", "Verträglichkeit"]:
            werte = st.session_state.antworten.get(dimension, [])
            if len(werte) > 0 and None not in werte:
                score = sum(werte) / len(werte)
                st.subheader(f"{dimension}")
                st.progress(score / 7)
                st.write(f"**Durchschnittswert: {score:.2f}**")
            else:
                st.warning(f"Nicht alle Fragen für {dimension} wurden beantwortet.")


elif seite == "Berufsempfehlung":
    st.title("Berufsempfehlung basierend auf Ihrem Big-Five-Profil und persönlichen Angaben")

    if not st.session_state.get("antworten"):
        st.warning("Bitte füllen sie den Fragebogen aus.")
    
    else: 
        werte = {k: sum(v)/len(v) for k, v in st.session_state.antworten.items()}

        st.divider()
    
    if "Name" not in st.session_state or "Alter" not in st.session_state or "Geschlecht" not in st.session_state:
        st.warning("Bitte füllen Sie zuerst den Fragebogen aus.")
    else:
        alter = st.session_state["Alter"]
        geschlecht_text = st.session_state["Geschlecht"]
        geschlecht_code = {"Männlich": 0, "Weiblich": 1, "Divers": 0.5}.get(geschlecht_text, 0)
    
    
    scores = {
        "Akademischer Bereich": (
            -0.3 * werte["Extraversion"] +
            0.1 * werte["Neurotizismus"] +
            0.8 * werte["Offenheit"] +
            0.6 * werte["Gewissenhaftigkeit"] +
            -0.1 * werte["Verträglichkeit"] +
            0.2 * alter + 
            0.2* geschlecht_code +
            0.2   
        ),
        "Dienstleistungen": (
            -0.3 * werte["Extraversion"] +
            0.1 * werte["Neurotizismus"] +
            0.8 * werte["Offenheit"] +
            0.6 * werte["Gewissenhaftigkeit"] +
            -0.1 * werte["Verträglichkeit"] +
            0.2 * alter + 
            0.2* geschlecht_code +
            0.2 
        ),
        "Führungskraft": (
            -0.3 * werte["Extraversion"] +
            0.1 * werte["Neurotizismus"] +
            0.8 * werte["Offenheit"] +
            0.6 * werte["Gewissenhaftigkeit"] +
            -0.1 * werte["Verträglichkeit"] +
            0.2 * alter + 
            0.2* geschlecht_code +
            0.2 
        ),
        "Handwerkerlicher Bereich":(
            -0.3 * werte["Extraversion"] +
            0.1 * werte["Neurotizismus"] +
            0.8 * werte["Offenheit"] +
            0.6 * werte["Gewissenhaftigkeit"] +
            -0.1 * werte["Verträglichkeit"] +
            0.2 * alter + 
            0.2* geschlecht_code +
            0.2 
        ),
        "Büroarbeiter": (
            -0.3 * werte["Extraversion"] +
            0.1 * werte["Neurotizismus"] +
            0.8 * werte["Offenheit"] +
            0.6 * werte["Gewissenhaftigkeit"] +
            -0.1 * werte["Verträglichkeit"] +
            0.2 * alter + 
            0.2* geschlecht_code +
            0.2  
        ),
        "Techniker":(
            -0.3 * werte["Extraversion"] +
            0.1 * werte["Neurotizismus"] +
            0.8 * werte["Offenheit"] +
            0.6 * werte["Gewissenhaftigkeit"] +
            -0.1 * werte["Verträglichkeit"] +
            0.2 * alter + 
            0.2* geschlecht_code +
            0.2 
        )
    }

    bester_bereich = max(scores, key= scores.get)
    bester_score = scores[bester_bereich]

    st.header("Empfohlener Bereich basierend auf einer Regressionsanalyse")
    st.success(f" {bester_bereich} (Score: {bester_score:.2f})")
    with st.expander("🔍 Alle Score-Werte anzeigen"):
            for bereich, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                st.write(f"{bereich}: {score:.2f}")