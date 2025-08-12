import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#streamlit run "C:\Users\Dell\Documents\Python\survey_app.py"

descriptions = {
   "treatment": "*Haben Sie sich wegen einer psychischen Erkrankung in Behandlung begeben?*  \n" 
   "Diese Frage impliziert, das bei den Personen eine psychische Krankheit vorliegt.",
   "benefits": "Bietet Ihr Arbeitgeber Leistungen für psychische Gesundheit an?",
   "care_options":"Kennen Sie die Möglichkeiten der psychosozialen Versorgung, die Ihr Arbeitgeber anbietet?",
   "wellness_program": "Hat Ihr Arbeitgeber jemals über psychische Gesundheit als Teil eines Wellness-Programms für Mitarbeiter gesprochen?",
   "seek_help":"Stellt Ihr Arbeitgeber Möglichkeiten zur Verfügung, um mehr über psychische Probleme zu erfahren und wie man Hilfe sucht?",
   "anonymity":"Ist Ihre Anonymität geschützt, wenn Sie sich dafür entscheiden, eine Behandlung für psychische Gesundheit oder Drogenmissbrauch in Anspruch zu nehmen?",
   "leave":"Wie einfach ist es für Sie, sich wegen einer psychischen Erkrankung krankschreiben zu lassen?",
   "mental_health_consequence":"Glauben Sie, dass es negative Folgen haben könnte, wenn Sie mit Ihrem Arbeitgeber über ein psychisches Problem sprechen?",
   "coworkers":"Wären Sie bereit, mit Ihren Kollegen über ein psychisches Problem zu sprechen?",
   "supervisor":"Wären Sie bereit, mit Ihren direkten Vorgesetzten über ein Problem der psychischen Gesundheit zu sprechen?",
   "mental_health_interview":"Glauben Sie, dass es negative Folgen haben könnte, wenn Sie mit Ihrem Arbeitgeber über ein psychisches Problem sprechen?",
   "phys_health_interview":"Glauben Sie, dass es negative Folgen haben könnte, wenn Sie mit Ihrem Arbeitgeber über ein gesundheitliches Problem sprechen?",
   "mental_vs_physical":"Haben Sie das Gefühl, dass Ihr Arbeitgeber die psychische Gesundheit genauso ernst nimmt wie die körperliche?",
   "mental_health_condition":"Haben sie mentale Probleme?  \n"
   "Hinweis: *Diese Variable wurde durch die Variable work_interfere und treatment ermittelt.*",
   "obs_consequence": "Haben Sie von negativen Folgen für Mitarbeiter mit psychischen Erkrankungen an Ihrem Arbeitsplatz gehört oder diese beobachtet?",
   "phys_health_consequence": "Glauben Sie, dass es negative Folgen haben könnte, wenn Sie mit Ihrem Arbeitgeber über ein gesundheitliches Problem sprechen?",

}

st.set_page_config(page_title="Mental Health in Tech - Dashboard", layout="centered")

df = pd.read_csv("C:/Users/Dell/Documents/Python/hr_project/survey_clean.csv")
df = df.drop(df[["Timestamp", "comments"]],axis= 1)


seite = st.sidebar.radio("Navigation", ["Variablen-Verteilungen", "Hypothesen und Ergebnisse"])
st.title("Mentale Gesundheit in der technischen Industrie")

if seite == "Variablen-Verteilungen":
    column = st.selectbox("Wähle eine Variable zur Anzeige:", df.columns)

    st.subheader(f"Verteilung von: {column}")

    if column == "Age":
        fig = px.histogram(df, x = "Age", nbins=30, title="Allgemeine Verteilung des Alters")

        st.plotly_chart(fig)

    elif column == "Gender":
        gender_count = df["Gender"].value_counts().reset_index()
        gender_count.columns = ["Gender", "Count"]

        fig = px.pie(gender_count, values="Count", names="Gender", 
        title="Geschlechterverteilung", 
        hover_data=["Count"], 
        labels={"Count": "Anzahl"}).update_traces(textinfo="percent+label")
        st.plotly_chart(fig)

    elif column == "Country":
        Country_big = df.Country.value_counts().head(9).index
        df["Country"] = df["Country"].apply(lambda x: x if x in Country_big else "Other")

        country_count = df["Country"].value_counts().reset_index()
        country_count.columns = ["Country","count"]

        fig = px.pie(country_count, values="count", names="Country", 
        title="Länderverteilung", 
        hover_data=["count"], 
        labels={"count": "Anzahl"}).update_traces(textinfo="percent+label")
        st.plotly_chart(fig)

    elif column == "work_interfere":
        interfere_count = df["work_interfere"].value_counts(normalize= True, sort= False)
        st.markdown(
            "*Wenn Sie an einer psychischen Erkrankung leiden, haben Sie das Gefühl, dass diese Ihre Arbeit beeinträchtigt?*  \n"
            "Hinweis: Not applicable wurde hinzugefügt, da eine Beantwortung impliziert, das die Befrageten psychische Probleme haben."
        )
        fig = px.bar(
            x = interfere_count.index,
            y = interfere_count.values,
            labels = {"x": "work_interfere", "y": "Anteil"},
            range_y= [0,0.5]
        )
        st.plotly_chart(fig)

    elif column == "no_employees":
        number_order = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
        df["no_employees"] = pd.Categorical(df["no_employees"], categories=number_order, ordered=True)
        employee_count = df["no_employees"].value_counts(normalize = True, sort = False)

        fig = px.bar(
            x = employee_count.index,
            y = employee_count.values,
            labels = {"x": "Anzahl der Mitarbeiter", "y": "Anteil"},
            range_y= [0,0.5]
        )
        st.plotly_chart(fig)

    else: 

        if column in descriptions:
            st.markdown(f"{descriptions[column]}")
        chart_type = st.radio("Diagrammtyp:", ["Balkendiagramm", "Kreisdiagramm"])

        if chart_type == "Balkendiagramm":
            value_type = st.radio("Anzeige:",["Anzahl", "Prozentanteil"])

            if value_type == "Anzahl":
                counts = df[column].value_counts(sort= False)
            else: 
                counts = df[column].value_counts(normalize= True, sort= False)

            fig = px.bar(
                x = counts.index, 
                y = counts.values, 
                labels = {"x": column,"y": "Anteil" if value_type == "Prozentanteil" else "Anzahl"},
                title= f"{column}-Balkendiagramm"
            )
            st.plotly_chart(fig)

        elif chart_type == "Kreisdiagramm":
            column_count = df[column].value_counts().reset_index()
            column_count.columns = [column, "count"]
        
            fig = px.pie(
                column_count,
                names= column, 
                values= "count",
                title = f"{column}-Kreisdiagramm",
                hover_data=["count"], 
                labels={"count": "Anzahl"}
            ).update_traces(textinfo= "percent + label")

            st.plotly_chart(fig)
        else:
            st.warning("Diese Variable ist nicht geeignet zur Visualisierung.")

elif seite == "Hypothesen und Ergebnisse":

    hypothesen = {
        "H1: Mit dem Alter steigt die Bereitschaft mentale Probleme mit zu teilen.": {
            "beschreibung":"Es wird untersucht ob die Personen offener über Probleme reden, wenn sie älter werden.",
            "motivation":"Ältere Beschäftigte verfügen möglicherweise über mehr Lebenserfahrung, was sich in einer größeren Offenheit gegenüber psychischer Gesundheit widerspiegeln kann.\n\n"
                        "Zudem könnten sie sich in ihrer beruflichen Position sicherer fühlen, wodurch die Angst vor Stigmatisierung geringer ausfällt.",
            "ergebnisse":"Die logistische Regression ergibt das die Effektstärke gering ist und kein signifikanter Zusammenhang besteht. Die Hypothese wird verworfen."
        },
        "H2: Mit zunehmenden Alter steigt die Wahrscheinlichkeit mentale Probleme zu haben.": {
            "beschreibung":"Steigt mit zunehmenden Alter die Wahrscheinlichkeit mentaler Probleme?",
            "motivation":"Die Verteilung der Daten ist rechtsschief: Während die Anzahl älterer Mitarbeitender insgesamt abnimmt, scheint der Anteil psychischer Erkrankungen in dieser Gruppe vergleichsweise höher zu sein.\n\n"
                        "Dies kann verschiedene Gründe haben: Einerseits könnten Personen, die psychische Gesundheit als relevantes Thema empfinden oder selbst betroffen sind, eher zur Teilnahme an der Befragung neigen.\n\n"
                        "Andererseits nehmen mit dem Alter potenziell belastende Lebensereignisse (z. B. Todesfälle im nahen Umfeld) zu, die das Auftreten mentaler Probleme begünstigen können.",
             "ergebnisse":"Die logistische Regression ergibt das ein signifikanter Zusammenhang besteht. Allerdings sei zu erwähnen, das die Effektstärke gering ist."
        },
        "H3: Männer sind ihrem Vorgesetzten offener hinsichtlich ihren psychischen Zustandes.": {
            "beschreibung":"Es wird untersucht ob es geschlechtliche Unterschiede hinsichtlich der Kommunikation psychischer Krankheiten gibt.",
            "motivation":"Die Abbildung zeigt, dass sich der Anteil kommunikativer Offenheit gegenüber Kolleg:innen zwischen den Geschlechtern kaum unterscheidet.\n\n"
                        "Allerdings fällt ein Unterschied im Hinblick auf die Kommunikation mit Vorgesetzten auf:\n"
                        "Der größte Anteil der Männer gibt an, offen mit Führungspersonen über psychische Probleme sprechen zu können – ein Muster, das bei den anderen Geschlechtern weniger stark ausgeprägt ist (siehe Abbildungen in Zeile 1).",
            "ergebnisse":"Die Regressionen ergeben signifikante Koeffizenten für die Kommunikation mit Vorgesetzten. Allerdings nicht für die Kommunikation mit Kollegen. Zusammenfassend lässt sich festhalten:  \n\n"
            "Männer geben mit signifikant höherer Wahrscheinlichkeit an, dass sie mit ihren Vorgesetzten über mentale Probleme sprechen können, verglichen mit Frauen. \n\n"
            "Interpretation:\n\n"
            "Das Ergebnis liegt nahe, das Männer im Vergleich zu Frauen eher zu einer **totalen Offenheit**, statt einer Selektion der Ansprechpartner tendieren. Es könnte ein starker Entweder-Oder-Effekt (Ja oder Nein) vorliegen."
        },
        "H4: Die Wahrscheinlichkeit einer psychischen Erkrankungen ist bei Frauen und Diversen höher.": {
            "beschreibung":"Gibt es geschlechtliche Unterschiede hinsichtlich der Wahrscheinlichkeit einer psychischen Erkrankung?",
            "motivation":"In der Darstellung ist ersichtlich, dass psychische Erkrankungen bei allen Geschlechtern häufiger vorkommen als nicht – besonders bei Frauen und Personen, die sich als divers identifizieren.\n\n"
                        "Aus psychologischer Sicht ist bekannt, dass Frauen häufiger unter Depressionen und Angststörungen leiden – mögliche Ursachen sind hormonelle Schwankungen, gesellschaftliche Belastungen oder unterschiedliche Hilfesuchverhalten.",
            "ergebnisse":"Der Effekt ist hochsignifikant und negativ. Bedeutet:\n\n"
            "Frauen und Diverse sind häufiger von psychischen Erkrankungen betroffen."
        },
        "H5: Das Fehlen familiärer Vorerkrankungen ist ein guter Prädiktor für die allgemeine Gesundheit – jedoch nicht für das Auftreten psychischer Erkrankungen.": {
            "beschreibung":"Es wird untersucht ob psychische Vorerkrankung in der Familie ein Prädiktor ist.",
            "motivation":"Das rechte Kreisdiagramm zeigt die familiäre Vorgeschichte von Personen mit psychischer Erkrankung.\n\n"
                        "Im linken Diagramm erkennt man, dass 83,7\% der Personen **ohne** psychische Erkrankung auch **keine** familiäre Vorbelastung angeben.\n\n"
                        "Bei den erkrankten Personen (rechtes Diagramm) sind die Verhältnisse deutlich ausgeglichener.\n\n"
                        "Daraus lässt sich ableiten, dass das Fehlen familiärer Vorerkrankungen ein **guter Prädiktor für allgemeine psychische Stabilität** ist – jedoch nicht ausschließt, dass eine psychische Erkrankung dennoch auftritt.",
            "ergebnisse":"Die Regression ergibt einen höchst signifikanten positiven Effekt. Die Hypothese ist bestätigt. Somit gilt:\n\n"
            "**Das Fehlen familiärer Vorerkrankungen ist ein guter Prädiktor für die allgemeine Gesundheit.**"
        },
        "H6: Kommunikation - Unternehmensgröße": {
            "beschreibung":"Wie entwickelt sich die Kommunikation von Problemen mit steigender Unternehmensgröße.",
            "motivation":"In großen Unternehmen sind Entscheidungswege länger und der Arbeitsalltag stärker in funktionale Einheiten unterteilt, wodurch die Anonymität steigt.\n\n"
                        "In kleineren Unternehmen hingegen sind die Strukturen persönlicher, die Kommunikationswege kürzer – was zu einer höheren Offenheit führen kann.\n\n"
                        "Daraus ergibt sich die Annahme, dass Mitarbeitende in kleinen Unternehmen sich tendenziell stärker in den Extremen äußern (Yes/No), während bei großen Unternehmen häufiger ambivalente oder zurückhaltende Antworten gegeben werden.",
            "ergebnisse":"Die Ergebnisse ergeben signifikante Ergebnisse für Kollegen und Vorgesetzte.\n\n"
            "Kollegen: In größeren Unternehmen kann man eher mit allen reden, im Vergleich mit niemanden reden zu können. Die Wahrscheinlichkeit mit Allen über die Probleme reden zu können, nimmt mit steigender Unternehmensgröße ab. Die Wahrscheinlichkeit mit keinem reden zu können nimmt zu.\n\n"
            "Zusammenfassend kann man festhalten: **Mit steigender Unternehmensgröße die Anonymität und Distanz anwachsen und die Offenheit sinkt.** \n\n"
            "Vorgesetzte: Analog ist die Interpretation für die Vorgesetzten, auch hier gilt: "
            "**Mit steigender Unternehmensgröße die Anonymität und Distanz anwachsen und die Offenheit sinkt.**"
        },
        "H7: Quotient....": {
            "beschreibung":"jaaaaaa machen wir dann xd"
        },
    }

    auswahl = st.selectbox("Wählen Sie eine Hypothese:", list(hypothesen.keys()))

    info = hypothesen[auswahl]
    st.subheader(auswahl)
    st.markdown(f"*{info["beschreibung"]}*")

    if auswahl == "H2: Mit zunehmenden Alter steigt die Wahrscheinlichkeit mentale Probleme zu haben.":
        mental_age = (df.groupby(["Age", "mental_health_condition"]).size().reset_index(name = "count"))
        fig = px.bar(mental_age, x = "Age",y = "count",color = "mental_health_condition", title="Vertreilung des Alters hinsichtlich psychische Probleme", barmode= "stack")
        st.plotly_chart(fig)
        with st.expander("Warum ist das relevant?"):
            st.markdown(info["motivation"])
        with st.expander("Ergebnisse"):
            st.markdown(info["ergebnisse"])

    elif auswahl == "H1: Mit dem Alter steigt die Bereitschaft mentale Probleme mit zu teilen.":
        category_order = ["No", "Some of them", "Yes"]
        df["coworkers"] = pd.Categorical(df["coworkers"], categories=category_order, ordered=True)

        
        df["Age_bin"] = pd.cut(df["Age"], bins=range(18, 71, 5))

        
        grouped = df.groupby(["Age_bin", "coworkers"]).size().reset_index(name="count")

        
        grouped["total"] = grouped.groupby("Age_bin")["count"].transform("sum")
        grouped["percent"] = grouped["count"] / grouped["total"] * 100

        grouped["Age_bin"] = grouped["Age_bin"].astype(str)

        
        fig = px.area(
            grouped,
            x="Age_bin",
            y="percent",
            color="coworkers",
            category_orders={"coworkers": category_order},
            line_group="coworkers",
            groupnorm='percent',
            labels={"percent": "Anteil (%)", "Age_bin": "Alter"},
            title="Kumulative Kommunikation mit Kollegen nach Alter"
        )

        fig.update_layout(yaxis_ticksuffix="%", hovermode="x unified")
        st.plotly_chart(fig)

        with st.expander("Warum ist das relevant?"):
            st.markdown(info["motivation"])
        with st.expander("Ergebnisse"):
            st.markdown(info["ergebnisse"])

    elif auswahl == "H3: Männer sind ihrem Vorgesetzten offener hinsichtlich ihren psychischen Zustandes.":
        gender_supervisor = (df.groupby(["Gender", "supervisor"]).size().reset_index(name= "count"))
        gender_coworkers = (df.groupby(["Gender", "coworkers"]).size().reset_index(name= "count"))
        gender_list = ["male", "female", "diverse"]
        fig = make_subplots(rows=2, cols=3,
                    specs=[[{'type':'domain'}]*3, [{'type':'domain'}]*3],
                    subplot_titles=[
                        f"Supervisor - {gender}" for gender in gender_list
                    ] + [
                        f"Coworkers - {gender}" for gender in gender_list
                    ])

        for i, gender in enumerate(gender_list):
            data = gender_supervisor[gender_supervisor["Gender"] == gender]
            fig.add_trace(
                go.Pie(labels= data["supervisor"], values=data["count"], name = f"{gender} Supervisor"),
                row = 1, col= i+1
            )

        for i, gender in enumerate(gender_list):
            data = gender_coworkers[gender_coworkers["Gender"]==gender]
            fig.add_trace(
                go.Pie(labels= data["coworkers"], values=data["count"], name = f"{gender} Coworkers"),
                row=2, col=i+1
            )

        fig.update_layout(
            title_text = "Kommunikationsverhalten zu Vorgesetzten und Kollegen nach Geschlecht",
            height = 700
        )


        st.plotly_chart(fig)
        with st.expander("Warum ist das relevant?"):
            st.markdown(info["motivation"])
        with st.expander("Ergebnisse"):
            st.markdown(info["ergebnisse"])

    elif auswahl == "H4: Die Wahrscheinlichkeit einer psychischen Erkrankungen ist bei Frauen und Diversen höher.":
        gender_mhc = (df.groupby(["Gender", "mental_health_condition"]).size().reset_index(name = "count"))
        fig = px.pie(gender_mhc, values= "count", facet_col="Gender", color= "mental_health_condition")

        fig.update_layout(
        title ={
        "text": "Psychische Erkrankungen der Geschlechter <span style=\"color:dodgerblue\">(Dunkelblau = Erkrankung)</span>"
        }
        )

        st.plotly_chart(fig)
        with st.expander("Warum ist das relevant?"):
            st.markdown(info["motivation"])
        with st.expander("Ergebnisse"):
            st.markdown(info["ergebnisse"])

    elif auswahl == "H5: Das Fehlen familiärer Vorerkrankungen ist ein guter Prädiktor für die allgemeine Gesundheit – jedoch nicht für das Auftreten psychischer Erkrankungen.":
        mental_family = df.groupby(["mental_health_condition", "family_history"]).size().reset_index(name= "count")

        fig = px.pie(mental_family, values= "count", facet_col= "mental_health_condition", color= "family_history")

        fig.update_layout(
        title ={
        "text": "Familiengeschichte nach Psychischer Erkrankung <span style=\"color:dodgerblue\">(Dunkelblau = Psychische Erkrankung in der Familie)</span>"
        }
        )
        st.plotly_chart(fig)
        with st.expander("Warum ist das relevant?"):
            st.markdown(info["motivation"])
        with st.expander("Ergebnisse"):
            st.markdown(info["ergebnisse"])
    
    elif auswahl == "H6: Kommunikation - Unternehmensgröße":
        number_order = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
        df["no_employees"] = pd.Categorical(df["no_employees"], categories= number_order, ordered= True )
        fig = px.histogram(
            df,
            x="no_employees",
            color="coworkers", 
            barmode="relative",  
            histfunc="count",
            title="Kommunikation mit Kolleg:innen nach Unternehmensgröße",
            category_orders={"no_employees": number_order}
        ) 

        st.plotly_chart(fig)
        with st.expander("Warum ist das relevant?"):
            st.markdown(info["motivation"]) 
        with st.expander("Ergebnisse"):
            st.markdown(info["ergebnisse"])


