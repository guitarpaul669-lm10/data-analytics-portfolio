import streamlit as st
import webbrowser

# --- Seitenkonfiguration ---
st.set_page_config(page_title="Mein Data Analytics Portfolio", layout="wide")


st.title("📊 Mein Data Analytics Portfolio")
st.markdown("""
Willkommen!  
Hier findest du eine Auswahl der Data-Analytics-Projekte mit interaktiven Dashboards, Analysen und Visualisierungen.
""")
st.markdown("[💻 Programmier-Badges auf Hackerrank in SQL und Python](https://www.hackerrank.com/profile/guitarpaul669)")


# --- Navigation über Tabs ---
tab1, tab2, tab3 = st.tabs(["🛒 Projekt 1", "🧑‍⚕️ Projekt 2", " 🗒 Projekt 3"])

# ============================
# PROJEKT 1
# ============================
with tab1:
    st.header("Projekt 1 – E-Commerce Analyse")
    st.markdown("""
    **Kurzbeschreibung:**  
    Analyse eines großen E-Commerce-Datensatzes mit Fokus auf Bestellverhalten, Anbieter, Kunden, Standorte, Lieferzeiten und Korrelationen.
    """)
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[🔗 Streamlit App öffnen](https://data-analytics-portfolio-e-commerce.streamlit.app)")
    with col2:
        st.markdown("[💻 Code auf GitHub](https://github.com/guitarpaul669-lm10/data-analytics-portfolio/blob/main/Portfolio/notebooks/Brazil-E-Commerce.ipynb)")

# ============================
# PROJEKT 2
# ============================
with tab2:
    st.header("Projekt 2 – Psychische Gesundheit in der technischen Industrie")
    st.markdown("""
    **Kurzbeschreibung:**  
    Analyse eine Tech-Survey mit Fokus auf Ursachen und Zusammenhänge. Durch die Datenanalyse konnten Hypothesen gebildet werden und mit Regressionen untersucht werden.
    """)
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[🔗 Streamlit App öffnen](https://data-analytics-portfolio-survey.streamlit.app)")
    with col2:
        st.markdown("[💻 Code auf GitHub](https://github.com/guitarpaul669-lm10/data-analytics-portfolio/blob/main/Portfolio/notebooks/survey.ipynb)")

# ============================
# PROJEKT 3
# ============================
with tab3:
    st.header("Projekt 3 – Zusammenhang BIG FIVE (Persönlichkeitsfaktoren) mit der Jobzufriedenheit für verschiedene Arbeitsbereiche")
    st.markdown("""
    **Kurzbeschreibung:**  
    Auf Grundlage der Bachelorarbeit und der berechneten Regressionen, wird dieses Thema interaktiv visualisiert in einer Streamlit-App. Die Daten stammen vom Sozio-oekonomisches Panel (SOEP).
    """)
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[🔗 Streamlit App öffnen](https://data-analytics-portfolio-bigfive.streamlit.app)")
    with col2:
        st.markdown("[💻 Code auf GitHub](https://github.com/guitarpaul669-lm10/data-analytics-portfolio/blob/main/Portfolio/notebooks/Job%20Zufriedenheit.R)")




