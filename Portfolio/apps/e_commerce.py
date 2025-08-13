import streamlit as st
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.subplots as sp
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.title("E-Commerce Analyse Übersicht")

analyse = [
    "1. Welche Produkte sind am beliebtesten?",
    "2. Regionale vs. saisonale Verkaufsmuster",
    "3. Top Kunden",
    "4. Top Anbieter",
    "5. Durchschnittlicher Warenkorbwert und Produktanzahl",
    "6. Abgebrochene Bestellungen (Hinweise und Muster)",
    "7. Review-Score",
    "8. Zusammenhänge der Variablen Lieferzeit, Versandkosten, Standorte"
]

auswahl = st.selectbox("Wählen Sie eine Analyse:", analyse)

if auswahl == "1. Welche Produkte sind am beliebtesten?":
	sql_query = """
    SELECT pr.product_category_name, 
    it.product_id,
    COUNT(it.product_id) AS product_count 
    FROM item it
    LEFT JOIN products pr ON it.product_id = pr.product_id
    GROUP BY pr.product_category_name, it.product_id
    ORDER BY product_count DESC
    LIMIT 10;
    """ 
    url = "https://drive.google.com/uc?export=download&id=1oQqqWleQTWuhYNJMM_i_J60qFYsy1oCV"
    df = pd.read_csv(url)
    top10 = df["product_category_name"].value_counts(normalize=True).head(10)
    top10_df = top10.reset_index()
    top10_df.columns = ["product_category_name", "share"]

    # Plot
    fig = px.bar(
        top10_df,
        x="share",
        y="product_category_name",
        orientation="h",
        title="Top 10 Produktkategorien",
        labels={"share": "Anteil", "product_category_name": "Produktkategorie"},
        text="share"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Die Ergebnisse zeigen die beliebtesten 10 Produktkategorien. Die Produktkategorien sind sehr ausgeglichen und ähneln sich nicht. Dadurch erkennt man kein Muster über die angebotenen/bestellten Produkte.")
    st.subheader("Verwendete SQL-Query")
    st.code(sql_query, language="sql")
    
elif auswahl == "2. Regionale vs. saisonale Verkaufsmuster":
    sql_query = """
SELECT cu.customer_city,
COUNT(ord.order_id) AS cust_count,
ROUND(COUNT(ord.order_id) * 100.0 / SUM(COUNT(ord.order_id)) OVER (), 2) AS percent
FROM orders ord
LEFT JOIN customer cu ON ord.customer_id = cu.customer_id
GROUP BY cu.customer_city
ORDER BY cust_count DESC
LIMIT 10;
    """
    sql_query_2 = """
SELECT ord.month_pur,
COUNT(ord.order_id) AS month_count, 
ROUND(COUNT(ord.order_id) * 100.0 / SUM(COUNT(ord.order_id)) OVER (), 2) AS percent
FROM orders ord
GROUP BY ord.month_pur
ORDER BY month_pur;
    """
    sql_query_3 = """
SELECT DAY(str_to_date(ord.order_purchase_timestamp, '%Y-%m-%d %H:%i:%s')) AS day_only, 
COUNT(ord.order_id) AS day_count,
ROUND(COUNT(ord.order_id)*100.0/ SUM(COUNT(ord.order_id)) OVER (), 2) AS percent
FROM orders ord
GROUP BY day_only
ORDER BY percent DESC;
    """
    url = "https://drive.google.com/uc?export=download&id=1xoyVRaqaawTHxmGVpQDsIkx0NvBJ3NxA"
    df = pd.read_csv(url)
    st.subheader("Kundenstandorte")
    top_place = df["customer_city"].value_counts(normalize=True).head(10)
    top_place_df = top_place.reset_index()
    top_place_df.columns = ["customer_city", "share"]
    fig = px.bar(top_place_df, x = "customer_city", y="share", title="Top 10 Städte", labels={"share":"Anteil", "cutomer_city": "Kundenstandorte"}, text = "share")
    fig.update_layout(yaxis = {"categoryorder":"total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Die Ergebnisse deuten darauf hin, das sich die meisten Kunden aus den Großstädten kommen.**")
    st.subheader("Verwendete SQL-Query")
    st.code(sql_query, language="sql")
    st.subheader("Saisonale Bestellmuster")
    grouped_month = df.copy()
    grouped_month = grouped_month.groupby("month_pur")["order_id"].count().reset_index().sort_values(by="month_pur", ascending= True)
    grouped_month.columns = ["month_pur", "order_count"]
    grouped_month["month_pur"] = grouped_month["month_pur"].astype(str)
    fig_2 = px.line(
    grouped_month,
    x="month_pur",
    y="order_count",
    markers=True,
    title="Bestellungen pro Monat"
    )
    fig_2.update_layout(xaxis_title="Monat", yaxis_title="Anzahl Bestellungen")
    st.plotly_chart(fig_2)
    st.markdown("**Im Sommer bestellen die meisten Personen. Weihnachtsbestellungen und andere Kaufmuster sind nicht beobachtbar.**")
    st.subheader("Verwendete SQL-Query")
    st.code(sql_query_2, language = "sql")
    df["order_purchase_timestamp"]= pd.to_datetime(df["order_purchase_timestamp"])
    df["day_pur"] = df["order_purchase_timestamp"].dt.day
    less_order = ["28","29","30","31"]
    grouped_day = df.copy()
    grouped_day = grouped_day.groupby("day_pur")["order_id"].count().reset_index().sort_values(by="day_pur", ascending= True)
    grouped_day.columns = ["day_pur", "order_count"]
    grouped_day["day_pur"] = grouped_day["day_pur"].astype(str)
    grouped_day["color"] = grouped_day["day_pur"].apply(lambda x: "red" if x in less_order else "blue")
    fig_3 =px.bar(grouped_day, x = "day_pur", y = "order_count",title="Bestellungen im Monat", labels ={"day_pur": "Monatstag", "order_count": "Anzahl der Bestellungen"}, text="order_count", color= "color")
    fig_3.update_layout(showlegend=False)
    st.plotly_chart(fig_3)
    st.markdown(
    "**Für die Tage lässt sich erkennen, dass die Personen Ende des Monats weniger bestellen.  \n"
    "Hier lassen sich wichtige Implikationen für Werbung und ähnliche Strategien ableiten.**"
    )
    st.subheader("Verwendete SQL-Query")
    st.code(sql_query_3, language = "sql")

elif auswahl == "3. Top Kunden":	
	sql_query = """
    SELECT DISTINCT cu.customer_unique_id,
    SUM(pa.payment_value) AS summe_bestellungen
    FROM customer cu
    LEFT JOIN orders ord ON ord.customer_id = cu.customer_id
    LEFT JOIN payment pa ON pa.order_id = ord.order_id
    GROUP BY cu.customer_unique_id
    ORDER BY summe_bestellungen DESC
    LIMIT 20;
    """
    sql_query_2 = """
    WITH top_customers AS(
    SELECT DISTINCT cu.customer_unique_id,
    SUM(pa.payment_value) AS summe_bestellungen
    FROM customer cu
    LEFT JOIN orders ord ON ord.customer_id = cu.customer_id
    LEFT JOIN payment pa ON pa.order_id = ord.order_id
    GROUP BY cu.customer_unique_id
    ORDER BY summe_bestellungen DESC
    LIMIT 20)
    SELECT cu.customer_state,
    COUNT(cu.customer_state) AS kundenanzahl
    FROM customer cu
    JOIN top_customers tc ON cu.customer_unique_id = tc.customer_unique_id
    GROUP BY cu.customer_state
    ORDER BY kundenanzahl DESC;
    """
    sql_query_3 = """
    WITH top_summe AS (
    SELECT cu.customer_unique_id,
	SUM(pa.payment_value) AS summe_bestellungen
    FROM customer cu
    LEFT JOIN orders ord ON ord.customer_id = cu.customer_id
    LEFT JOIN payment pa ON pa.order_id = ord.order_id
    GROUP BY cu.customer_unique_id
    ORDER BY summe_bestellungen DESC
    LIMIT 20
    ),
    top_anzahl AS (
    SELECT cu.customer_unique_id,
    COUNT(DISTINCT ord.order_id) AS anzahl_bestellungen
    FROM customer cu
    LEFT JOIN orders ord ON ord.customer_id = cu.customer_id
    LEFT JOIN payment pa ON pa.order_id = ord.order_id
    GROUP BY cu.customer_unique_id
    ORDER BY anzahl_bestellungen DESC
    LIMIT 20
    )
    SELECT s.customer_unique_id, 
    s.summe_bestellungen, 
    a.anzahl_bestellungen
    FROM top_summe s
    JOIN top_anzahl a 
    ON s.customer_unique_id = a.customer_unique_id;
    """
	top_summe = ["8d50f5eadf50201ccdcedfb9e2ac8455",
    "3e43e6105506432c953e165fb2acf44c",
    "ca77025e7201e3b30c44b472ff346268",
    "6469f99c1f9dfae7733b25662e7f1782",
    "1b6c7548a2a1f9037c1fd3ddfed95f33",
    "63cfc61cee11cbe306bff5857d00bfe4",
    "f0e310a6839dce9de1638e0fe5ab282a",
    "dc813062e0fc23409cd255f7f53c7074",
    "12f5d6e1cbf93dafd9dcc19095df0b3d",
    "47c1a3033b8b77b3ab6e109eb4d5fdf3",
    "5e8f38a9a1c023f3db718edcf926a2db",
    "4e65032f1f574189fb793bac5a867bbc",
    "b4e4f24de1e8725b74e4a1f4975116ed",
    "fe81bb32c243a86b2f86fbf053fe6140",
    "394ac4de8f3acb14253c177f0e15bc58",
    "56c8638e7c058b98aae6d74d2dd6ea23",
    "35ecdf6858edc6427223b64804cf028e",
    "74cb1ad7e6d5674325c1f99b5ea30d82",
    "de34b16117594161a6a89c50b289d35a",
    "7305430719d715992b00be82af4a6aa8"]
    top_anzahl = ["0a0a92112bd4c708ca5fde585afaa872",
    "da122df9eeddfedc1dc1f5349a1a690c",
    "763c8b1c9c68a0229c42c9fc6f662b93",
    "dc4802a71eae9be1dd28f5d788ceb526",
    "459bef486812aa25204be022145caa62",
    "ff4159b92c40ebe40454e3e6a7c35ed6",
    "4007669dec559734d6f53e029e360987",
    "eebb5dda148d3893cdaf5b5ca3040ccb",
    "48e1ac109decbb87765a3eade6854098",
    "c8460e4251689ba205045f3ea17884a1",
    "edde2314c6c30e864a128ac95d6b2112",
    "a229eba70ec1c2abef51f04987deb7a5",
    "edf81e1f3070b9dac83ec83dacdbb9bc",
    "fa562ef24d41361e476e748681810e1e",
    "ca27f3dac28fb1063faddd424c9d95fa",
    "5e713be0853d8986528d7869a0811d2b",
    "58483a1c055dfb600f57c5b867174542",
    "011875f0176909c5cf0b14a9138bb691",
    "f0767ae738c3d90e7b737d7b8b8bb4d1",
    "bc5e25094a7d51b6aee35236572e64f4"]
	gemeinsam = list(set(top_summe) & set(top_anzahl))
    url = "https://drive.google.com/uc?export=download&id=1Slc8-E9E6RIqWc46DtQzM_pt4qe-EXxV"
    url_1 = "https://drive.google.com/uc?export=download&id=14nIEVTnY3CwcWCWXIPTX1K9euT5cTShC"
    df = pd.read_csv(url)
    cust_geo = pd.read_csv(url_1)
    st.subheader("Differenzierung der Topkunden")
    st.markdown("Top Kunden können entweder nach der Bestellanzahl oder der Ausgaben eingeteilt werden.")
    df_gemeinsam = pd.DataFrame(gemeinsam, columns=["customer_unique_id"])
    st.dataframe(df_gemeinsam)
	st.markdown("**Der Vergleich beider Varianten ergibt das es keine Überschneidungen gibt.**")
    st.subheader("Verwendete SQL-Query")
	st.code(sql_query_3, language = "sql")
	wahl = st.radio("Analysegruppe wählen:",("Top Kunden nach Bestellwert", "Top Kunden nach Anzahl Bestellungen"))
		if wahl == "Top Kunden nach Bestellwert":
		    st.subheader("Top Kunden nach Payment Value")
		    customer_df = df.groupby("customer_unique_id")["payment_value"].sum().sort_values(ascending=False)
		    customer_df = customer_df.reset_index()
		    customer_df.columns = ["customer_unique_id", "payment_value"]
		    cust_df = customer_df.groupby("payment_value").count()
		    cust_df = cust_df.reset_index()
		    cust_df.columns = ["payment_value", "Count"]
		    fig = px.line(cust_df, x = "payment_value", y = "Count", title= "Verteilung der insgesamten Ausgaben", markers= False, labels= {"Count": "Anzahl", "payment_value": "Summe der Ausgaben"})
		    fig.update_layout(
		    xaxis_range=[0, 5000]
		    )
		    fig.add_vline(x=3826.80, line_width = 3, line_dash = "dash", line_color = "green", annotation_text = "Threshold der Top 20 Kunden", annotation_position = "top right")
		    st.plotly_chart(fig)
		    st.markdown("Der Großteil der Kunden bestellt nur eine geringe Menge und bei preisgünstige Produkte. Die Top 20 Kunden teilen sich zum einen in Leute die häufig bestellen und Personen, welche sehr teure Sachen einmalig bestellen.  \n"
		                "**Beispielsweise bezahlte der Top Kunde einmalig ein Auto für 13.664 Real. Somit wird das Kaufverhalten des Top Kundens nicht untersucht.**")
		    st.subheader("Verwendete SQL-Query")
		    st.code(sql_query, language="sql")
		    st.subheader("Herkunft der Kunden")
		    top_20_cust =  df.groupby("customer_unique_id")["payment_value"].sum().sort_values(ascending=False).head(20).index
		    top_cust_geo = cust_geo[cust_geo["customer_unique_id"].isin(top_20_cust)]
		    customers = go.Scattermapbox(
		    lat=cust_geo["cust_lat"],
		    lon=cust_geo["cust_lng"],
		    mode="markers",
		    marker=dict(size=6, color="blue"),
		    name="Kunden"
		    )
		    top_customers = go.Scattermapbox(
		    lat=top_cust_geo["cust_lat"],
		    lon=top_cust_geo["cust_lng"],
		    mode="markers",
		    marker=dict(size=8, color="red"),
		    name="Top Kunden"
		    )
		    fig = go.Figure()
		    fig.add_trace(customers) 
		    fig.add_trace(top_customers)
		    fig.update_layout(
		    mapbox = dict(
		        style = "open-street-map", 
		        center= dict(lat=-14.2350, lon=-51.9253),
		        zoom = 4
		    ), 
		    margin = {"r":0, "t":0, "l":0, "b":0},
		    height= 800
		    )
		    st.plotly_chart(fig)
		    st.markdown("**Der Großteil der Top Kunden kommen aus den Großstädten Brasiliens.**")
		    st.subheader("Verwendete SQL-Query")
		    st.code(sql_query_2, language = "sql")
		elif wahl == "Top Kunden nach Anzahl Bestellungen":
			st.subheader("Top Kunden nach Anzahl Bestellungen")
			df = df[df["customer_unique_id"].isin(top_anzahl)]
		    customer_df = df.groupby("customer_unique_id")["payment_value"].sum().sort_values(ascending=False)
		    customer_df = customer_df.reset_index()
		    customer_df.columns = ["customer_unique_id", "payment_value"]
		    cust_df = customer_df.groupby("payment_value").count()
		    cust_df = cust_df.reset_index()
		    cust_df.columns = ["payment_value", "Count"]
		    fig = px.line(cust_df, x = "payment_value", y = "Count", title= "Verteilung der insgesamten Ausgaben", markers= False, labels= {"Count": "Anzahl", "payment_value": "Summe der Ausgaben"})
		    fig.update_layout(
		    xaxis_range=[0, 5000]
		    )
		    fig.add_vline(x=3826.80, line_width = 3, line_dash = "dash", line_color = "green", annotation_text = "Threshold der Top 20 Kunden", annotation_position = "top right")
		    st.plotly_chart(fig)
		    st.markdown("Der Großteil der Kunden bestellt nur eine geringe Menge und bei preisgünstige Produkte. Die Top 20 Kunden teilen sich zum einen in Leute die häufig bestellen und Personen, welche sehr teure Sachen einmalig bestellen.  \n"
		                "**Beispielsweise bezahlte der Top Kunde einmalig ein Auto für 13.664 Real. Somit wird das Kaufverhalten des Top Kundens nicht untersucht.**")
		    st.subheader("Verwendete SQL-Query")
		    st.code(sql_query, language="sql")
		    st.subheader("Herkunft der Kunden")
		    top_20_cust =  df.groupby("customer_unique_id")["payment_value"].sum().sort_values(ascending=False).head(20).index
		    top_cust_geo = cust_geo[cust_geo["customer_unique_id"].isin(top_20_cust)]
		    customers = go.Scattermapbox(
		    lat=cust_geo["cust_lat"],
		    lon=cust_geo["cust_lng"],
		    mode="markers",
		    marker=dict(size=6, color="blue"),
		    name="Kunden"
		    )
		    top_customers = go.Scattermapbox(
		    lat=top_cust_geo["cust_lat"],
		    lon=top_cust_geo["cust_lng"],
		    mode="markers",
		    marker=dict(size=8, color="red"),
		    name="Top Kunden"
		    )
		    fig = go.Figure()
		    fig.add_trace(customers) 
		    fig.add_trace(top_customers)
		    fig.update_layout(
		    mapbox = dict(
		        style = "open-street-map", 
		        center= dict(lat=-14.2350, lon=-51.9253),
		        zoom = 4
		    ), 
		    margin = {"r":0, "t":0, "l":0, "b":0},
		    height= 800
		    )
		    st.plotly_chart(fig)
		    st.markdown("**Der Großteil der Top Kunden kommen aus den Großstädten Brasiliens.**")
		    st.subheader("Verwendete SQL-Query")
		    st.code(sql_query_2, language = "sql")
		
    


elif auswahl == "4. Top Anbieter":
    sql_query = """
    SELECT se.seller_id,
    COUNT( DISTINCT ord.order_id) AS Summe_bestellungen,
    ROUND(COUNT(DISTINCT ord.order_id) * 100.0 / SUM(COUNT( DISTINCT ord.order_id)) OVER (), 2) AS percent
    FROM seller se
    LEFT JOIN item it ON se.seller_id = it.seller_id
    LEFT JOIN orders ord ON ord.order_id = it.order_id
    GROUP BY se.seller_id
    ORDER BY percent DESC
    LIMIT 10;
    """
    sql_query_2 = """
    WITH top_sellers AS(
    SELECT se.seller_id,
    COUNT(DISTINCT ord.order_id) AS Summe_bestellungen,
    ROUND(COUNT( DISTINCT ord.order_id) * 100.0 / SUM(COUNT( DISTINCT ord.order_id)) OVER (), 2) AS percent
    FROM seller se
    LEFT JOIN item it ON se.seller_id = it.seller_id
    LEFT JOIN orders ord ON ord.order_id = it.order_id
    GROUP BY se.seller_id
    ORDER BY percent DESC
    LIMIT 10)
    SELECT pr.product_category_name,
    COUNT( DISTINCT ord.order_id) as Produkt_anzahl,
    ROUND(COUNT( DISTINCT ord.order_id) * 100.0 / SUM(COUNT( DISTINCT ord.order_id)) OVER (), 2) AS percent
    FROM orders ord
    LEFT JOIN item it ON it.order_id = ord.order_id
    LEFT JOIN products pr ON pr.product_id = it.product_id
    JOIN top_sellers ts ON ts.seller_id = it.seller_id
    GROUP BY pr.product_category_name
    HAVING pr.product_category_name IS NOT NULL
    ORDER BY percent DESC;
    """
    sql_query_3 = """
    WITH top_seller AS(
    SELECT se.seller_id,
    COUNT(DISTINCT ord.order_id) AS Summe_bestellungen,
    ROUND(COUNT(DISTINCT ord.order_id) * 100.0 / SUM(COUNT(DISTINCT ord.order_id)) OVER (), 2) AS percent
    FROM seller se
    LEFT JOIN item it ON se.seller_id = it.seller_id
    LEFT JOIN orders ord ON ord.order_id = it.order_id
    GROUP BY se.seller_id
    ORDER BY percent DESC
    LIMIT 1)
    SELECT pr.product_category_name,
    COUNT(DISTINCT ord.order_id) as Produkt_anzahl,
    ROUND(COUNT(DISTINCT ord.order_id) * 100.0 / SUM(DISTINCT COUNT(ord.order_id)) OVER (), 2) AS percent
    FROM orders ord
    LEFT JOIN item it ON it.order_id = ord.order_id
    LEFT JOIN products pr ON pr.product_id = it.product_id
    JOIN top_seller ts ON ts.seller_id = it.seller_id
    GROUP BY pr.product_category_name
    HAVING pr.product_category_name IS NOT NULL
    ORDER BY percent DESC;
    """
    url = "https://drive.google.com/uc?export=download&id=1Zj6RLYe6BRGWmzMH1eOij8zv64qYXZXJ"
    url_1 = "https://drive.google.com/uc?export=download&id=1hPoliAfXA4ETrRRyVZMuwVkPVa_pgY6a"
    df = pd.read_csv(url)
    seller_geo = pd.read_csv(url_1)
    st.subheader("Top Anbieter nach Anzahl der Bestellungen")
    top_10_seller =  df.groupby("seller_id")["order_id"].nunique().sort_values(ascending=False).head(10).index
    top_1_seller = df.groupby("seller_id")["order_id"].nunique().sort_values(ascending=False).head(1).index
    top_sell_geo = seller_geo[seller_geo["seller_id"].isin(top_10_seller)]
    seller = go.Scattermapbox(
    lat=seller_geo["seller_lat"],
    lon=seller_geo["seller_lng"],
    mode="markers",
    marker=dict(size=6, color="blue"),
    name="Verkäufer",
    text=seller_geo["seller_id"]
    )
    top_seller = go.Scattermapbox(
    lat=top_sell_geo["seller_lat"],
    lon=top_sell_geo["seller_lng"],
    mode="markers",
    marker=dict(size=8, color="red"),
    name="Top Verkäufer",
    text=top_sell_geo["seller_id"]
    )
    fig = go.Figure()
    fig.add_trace(seller) 
    fig.add_trace(top_seller)
    fig.update_layout(
    mapbox = dict(
        style = "open-street-map", 
        center= dict(lat=-14.2350, lon=-51.9253),
        zoom = 4
    ), 
    margin = {"r":0, "t":0, "l":0, "b":0},
    height= 800
    )
    st.plotly_chart(fig)
    st.markdown("**Beeindruckend ist das 50\% aller Anbieter weniger als 6 Bestellungen haben. Die größten Anbieter hingegen weisen über 1000 Bestellungen auf.**  \n"
                "Dementsprechend könnte der Handel durch bestimmte Anbieter monopolisiert werden.")
    st.subheader("Verwendete SQL-Query")
    st.code(sql_query, language="sql")
    st.subheader("Angebotene Produkte der besten 10 Produzenten")
    product_top10 = df[df["seller_id"].isin(top_10_seller)]
    product_top1 = df[df["seller_id"].isin(top_1_seller)]
    product_top10 = product_top10["product_category_name"].value_counts(normalize=True).sort_values(ascending=False).head(10)
    product_top1 = product_top1["product_category_name"].value_counts(normalize=True).sort_values(ascending=False).head(10)
    product_top10 = product_top10.reset_index()
    product_top1 = product_top1.reset_index()
    product_top10.columns = ["product_category_name", "share"]
    product_top1.columns = ["product_category_name", "share"]
    fig = px.bar(product_top10, x = "share", y = "product_category_name", orientation= "h", title= "Produktkategorien der besten 10 Anbieter", labels={"product_category_name":"Produktkategorien", "share":"Anteil"})
    st.plotly_chart(fig)
    fig = px.bar(product_top1, y = "product_category_name", x = "share", orientation= "h", title= "Produktkategorien des Top 1 Anbieter", labels={"product_category_name":"Produktkategorien", "share":"Anteil"})
    st.plotly_chart(fig)
    st.markdown("**Die Top-10-Anbieter sind deutlich breiter aufgestellt und verteilen ihre Produkte auf viele Kategorien, während der Top-1-Anbieter stark spezialisiert ist – über 80\% seines Angebots entfallen allein auf watches_gifts. Dadurch bedient er eine Nische, während die Top-10 insgesamt ein vielfältigeres Sortiment anbieten.**")
    st.subheader("Verwendete SQL-Query")
    st.markdown("Produktkategorien der Top 10")
    st.code(sql_query_2, language = "sql")
    st.markdown("Produktkategorien der Top 1")
    st.code(sql_query_3, language = "sql")
    st.subheader("Lieferzeiten der Top Seller")
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_time_diff"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
    delivery_top10 = df[df["seller_id"].isin(top_10_seller)]
    delivery_top1 = df[df["seller_id"].isin(top_1_seller)]

    fig = sp.make_subplots(rows=1, cols=3, subplot_titles=("Alle Verkäufer", "Top 10 Verkäufer", "Top 1 Verkäufer"))
    fig.add_trace(
        go.Violin(y=df["order_time_diff"], name="Alle", box_visible=True, meanline_visible=True),
        row=1, col=1
    )
    fig.add_trace(
    go.Violin(y=delivery_top10["order_time_diff"], name="Top 10", box_visible=True, meanline_visible=True),
    row=1, col=2
    )
    fig.add_trace(
    go.Violin(y=delivery_top1["order_time_diff"], name="Top 1", box_visible=True, meanline_visible=True),
    row=1, col=3
    )
    fig.update_layout(
    title="Lieferzeitenvergleich",
    showlegend=False,
    height=500,
    width=1200
    )
    st.plotly_chart(fig)
    st.markdown("Es lässt sich kein Unterschied zwischen allen und den Top 10 Anbietern erkennen.")
    st.markdown("**Jedoch überzeugt der Top Lieferant mit der schnellsten Lieferzeit in hohem Maße.**")
    
elif auswahl == "5. Durchschnittlicher Warenkorbwert und Produktanzahl":
    sql_query = """
    SELECT AVG(pa.payment_value)
    FROM payment pa
    LEFT JOIN orders ord ON pa.order_id = ord.order_id;
    """
    sql_query_2 = """
    SELECT AVG(it.order_item_id) AS avg_produktanzahl
    FROM customer cu
    LEFT JOIN orders ord ON ord.customer_id = cu.customer_id
    LEFT JOIN payment pa ON pa.order_id = ord.order_id
    LEFT JOIN item it ON it.order_id = ord.order_id;
    """
    url = "https://drive.google.com/uc?export=download&id=1Slc8-E9E6RIqWc46DtQzM_pt4qe-EXxV"
    df = pd.read_csv(url)
    st.subheader("Durchschnittlicher Warenkorbwert")
    wk_df = df.groupby("order_id")["payment_value"].sum()
    wk_df = wk_df.reset_index()
    wk_df.columns = ["order_id", "payment_value"]
    warenkorb_df = wk_df.groupby("payment_value").count()
    warenkorb_df = warenkorb_df.reset_index()
    warenkorb_df.columns = ["payment_value", "Count"]
    fig = px.line(warenkorb_df, x = "payment_value", y = "Count", title= "Warenkorbwert", markers= False)
    fig.update_layout(
    xaxis=dict(
        tickmode="linear",
        tick0=0,
        dtick=100
    ),
    xaxis_range=[0, 1000]
    )
    fig.add_vline(x=154.104831, line_width = 3, line_dash = "dash", line_color = "green", annotation_text = "Durchschnitt", annotation_position = "top right")
    st.plotly_chart(fig)
    st.markdown("**Der Warenkorbwert unterliegt einer hohen Streuung und reicht bis hin zu 13664.  \n"
    "Der Median beträgt 103.5.**")
    
    st.code(sql_query, language="sql")
    st.subheader("Durchschnittliche Produktanzahl")
    pa_df = df.groupby("order_id")["order_item_id"].max()
    pa_df = pa_df.reset_index()
    pa_df.columns = ["cust", "avg_value"]
    produktanzahl = pa_df["avg_value"].value_counts().reset_index()
    produktanzahl.columns = ["Produktanzahl", "Bestellungen"]  
    fig = px.bar(produktanzahl, x = "Produktanzahl", y= "Bestellungen", text = "Bestellungen")
    fig.add_vline(x=1.1964, line_width = 3, line_dash = "dash", line_color = "green", annotation_text = "Durchschnitt", annotation_position = "top right")
    st.plotly_chart(fig)
    st.subheader("Verwendete SQL-Query")
    st.markdown("**Die meisten Kunden bestellen nur ein Produkt pro Kauf.**")
    st.code(sql_query_2, language = "sql")

elif auswahl == "6. Abgebrochene Bestellungen (Hinweise und Muster)":
    sql_query = """
    SELECT DISTINCT ordna.customer_id,
    COUNT(ordna.customer_id) AS anzahl_bestellung
    FROM orders_na ordna
    GROUP BY ordna.customer_id
    ORDER BY anzahl_bestellung DESC;
    """
    sql_query_2 = """
    SELECT pa.payment_type,
    COUNT(*) as payment_anzahl
    FROM payment pa
    JOIN orders_na ordna ON ordna.order_id = pa.order_id
    GROUP BY pa.payment_type
    ORDER BY payment_anzahl DESC;
    """
    sql_query_3 = """
    SELECT pr.product_category_name,
    COUNT(ordna.order_id) as Produkt_anzahl,
    ROUND(COUNT(ordna.order_id) * 100.0 / SUM(COUNT(ordna.order_id)) OVER (), 2) AS percent
    FROM orders_na ordna
    LEFT JOIN item it ON it.order_id = ordna.order_id
    LEFT JOIN products pr ON pr.product_id = it.product_id
    GROUP BY pr.product_category_name
    HAVING pr.product_category_name IS NOT NULL
    ORDER BY percent DESC;
    """
    url = "https://drive.google.com/uc?export=download&id=1Slc8-E9E6RIqWc46DtQzM_pt4qe-EXxV"
    df = pd.read_csv(url)
    st.markdown("Verschiedene Aspekte wurden untersucht, ob bestimmte Haushalte immer die Bestellungen abbrechen,verschiedene Produkte zurückgeschickt werden, oder es an der Bezahlmethode gebunden ist.")
    st.subheader("Verwendete SQL-Query")
    st.subheader("Kunden")
    st.code(sql_query, language="sql")
    st.markdown("**Die abgebrochenen Bestellungen gehen nicht von einem Kunden oder Kundengruppe (Bsp.: gleicher Standort) aus.**")
    st.subheader("Lieferzeiten")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["time_difference"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
    fig = px.box(df, y= "time_difference", labels = {"time_difference": "Lieferzeit"}, title= "Lieferzeit abgebrochener Bestellungen")
    fig.update_layout(yaxis_range = [0,150])
    fig.add_hline(y=18, line_width = 1, line_dash = "dash", line_color = "green", annotation_text = "Durchschnitt abgebrochener Bestellungen", annotation_position = "top right")
    fig.add_hline(y=11.65, line_width = 1, line_dash = "dash", line_color = "red", annotation_text = "Durchschnitt aller Bestellungen", annotation_position = "bottom right")
    st.plotly_chart(fig)
    st.markdown("**Erfolgreiche Bestellungen werden im Durchschnitt eine Woche früher geliefert.  \n"
                "Das ist ein plausibler Grund, wieso Bestellung abgebrochen werden.**")
    st.subheader("Bezahlmethode")
    st.code(sql_query_2, language = "sql")
    st.markdown("**Die verwendeten Bezahlmethoden ähneln der Verteilung aller Bestellungen. Auch hier können keine Zusammenhänge ermittelt werden.**")   
    st.subheader("Produktarten")
    st.code(sql_query_3, language = "sql")
    st.markdown("**Bestimmte Produktkategorien sind auch keine Ursache für abgebrochene Bestellungen.**")
    

elif auswahl == "7. Review-Score":
    sql_query = """
    SELECT DISTINCT it.seller_id,
    AVG(review_score) AS avg_score
    FROM reviews re
    LEFT JOIN item it ON it.order_id = re.order_id
    GROUP BY it.seller_id
    ORDER BY avg_score DESC;
    """
    sql_query_2 = """
    SELECT DISTINCT it.seller_id,
    AVG(review_score) AS avg_score,
    COUNT(it.order_id) AS anzahl_bewertungen
    FROM reviews re
    LEFT JOIN item it ON it.order_id = re.order_id
    GROUP BY it.seller_id
    HAVING COUNT(it.order_id) > 5 AND avg_score >3
    ORDER BY avg_score DESC, COUNT(it.order_id) DESC;
    """
    sql_query_3 = """
    SELECT DISTINCT it.seller_id,
    AVG(review_score) AS avg_score,
    COUNT(it.order_id) AS anzahl_bewertungen
    FROM reviews re
    LEFT JOIN item it ON it.order_id = re.order_id
    GROUP BY it.seller_id
    HAVING COUNT(it.order_id) > 5 AND avg_score <3
    ORDER BY avg_score ASC, COUNT(it.order_id) DESC;
    """
    sql_query_4 = """
    WITH top_bewert AS(
    SELECT DISTINCT it.seller_id,
    AVG(review_score) AS avg_score,
    COUNT(it.order_id) AS anzahl_bewertungen
    FROM reviews re
    LEFT JOIN item it ON it.order_id = re.order_id
    GROUP BY it.seller_id
    HAVING COUNT(it.order_id) > 5 AND avg_score > 3
    ORDER BY avg_score DESC, COUNT(it.order_id) DESC
    )
    SELECT product_category_name,
    COUNT(product_category_name) AS anzahl_product
    FROM products pr
    JOIN item it on it.product_id = pr.product_id
    JOIN top_bewert top on top.seller_id = it.seller_id
    GROUP BY product_category_name
    ORDER By COUNT(product_category_name) DESC;
    """
    sql_query_5 = """
    WITH bad_bewert AS(
    SELECT DISTINCT it.seller_id,
    AVG(review_score) AS avg_score,
    COUNT(it.order_id) AS anzahl_bewertungen
    FROM reviews re
    LEFT JOIN item it ON it.order_id = re.order_id
    GROUP BY it.seller_id
    HAVING COUNT(it.order_id) > 5 AND avg_score <2
    ORDER BY avg_score ASC, COUNT(it.order_id) DESC
    )
    SELECT product_category_name,
    COUNT(product_category_name) AS anzahl_product
    FROM products pr
    JOIN item it on it.product_id = pr.product_id
    JOIN bad_bewert bad on bad.seller_id = it.seller_id
    GROUP BY product_category_name
    ORDER By COUNT(product_category_name) DESC;
"""
    url = "https://drive.google.com/uc?export=download&id=1TIydQgUz4dfnSQ_JwiSggCDTi6zJSzea"
    url_1 = "https://drive.google.com/uc?export=download&id=1EFi8r5aKaoeuiKoRVtHxAi3bZhpIVidW"
    url_2 = "https://drive.google.com/uc?export=download&id=1lH49hMawQhUtiP1sSpHivi1l7-IkLi2c"
    url_3 = "https://drive.google.com/uc?export=download&id=1dV25csezPVUhFENY4XKqwfYQf-jf1lC1"
    url_4 = "https://drive.google.com/uc?export=download&id=1aEs1tBSaQyAjsVONvbkAgL3lBMl9baAo"
    url_5 = "https://drive.google.com/uc?export=download&id=1YZARhhNH4xFhQljQP6bMdDkDJRpiML3F"
   
    df = pd.read_csv(url)
    df_2 = pd.read_csv(url_1)
    df_3 = pd.read_csv(url_2)
    bad_df = pd.read_csv(url_3)
    better_df = pd.read_csv(url_4)
    late_df = pd.read_csv(url_5)
    st.markdown("**Verschiedene Aspekte wurden untersucht, um herauszufinden was die Ursachen für gute und schlechte Bewertungen sind.**")
    st.subheader("Verteilungen mit Einschränkungen")
    st.markdown("Die Einschränkungen sind entscheidend für die Reduzierung von Verzerrungseffekten."
                "Beispielsweise ist eine Bewertung nicht aussagekräftig.")
    fig = px.box(df,y = "mean",title = "Durchschnittliche Bewertung", labels= {"mean": "Bewertungen"})
    st.plotly_chart(fig)
    st.markdown("**Der Bewertungsdurchschnitt beträgt 4.0864 Sterne.**")
    st.subheader("Verwendete SQL-Query")
    st.code(sql_query, language="sql")
    st.subheader("Top Anbieter vs. schlechte Anbieter nach Bewertungen")

    seller_better = go.Scattermapbox(
    lat=better_df["seller_lat"],
    lon=better_df["seller_lng"],
    mode="markers",
    marker=dict(size=6, color="blue"),
    name="Gute Bewertung"
    )

    seller_bad = go.Scattermapbox(
        lat=bad_df["seller_lat"],
        lon=bad_df["seller_lng"],
        mode="markers",
        marker=dict(size=6, color="red"),
        name="Schlechte Bewertung"
    )

    fig = go.Figure()
    fig.add_trace(seller_better)
    fig.add_trace(seller_bad)

    fig.update_layout(
        mapbox = dict(
            style = "open-street-map", 
            center= dict(lat=-14.2350, lon=-51.9253),
            zoom = 4
        ), 
        margin = {"r":0, "t":0, "l":0, "b":0},
        height= 800
    )
    st.plotly_chart(fig)
    st.markdown("**Es gibt sowohl viele Anbieter mit positiven, wie auch mit schlechten Bewertungen. Der Anteil der besseren Unternehmen überwiegt**")
    st.subheader("Verwendete SQL-Query")
    st.markdown("Gute Bewertungen")
    st.code(sql_query_2, language = "sql")
    st.markdown("Schlechte Bewertungen")
    st.code(sql_query_3, language = "sql")
    st.subheader("Produktarten")
    fig = px.bar(df_2.head(10), x = "proportion", y = "product_category_name", orientation= "h", title= "Produktkategorien der besten Anbieter", labels={"product_category_name":"Produktkategorien", "proportion":"Anteil"})
    st.plotly_chart(fig)
    st.subheader("Verwendete SQL-Query")
    st.code(sql_query_4, language = "sql")
    fig = px.bar(df_3.head(10), y = "product_category_name", x = "proportion", orientation= "h", title= "Produktkategorien der schlechten Anbieter", labels={"product_category_name":"Produktkategorien", "proportion":"Anteil"})
    st.plotly_chart(fig)
    st.code(sql_query_5, language = "sql")
    st.markdown("Die besten Anbieter weisen eine klare Fokussierung auf wenige Kernkategorien auf. Besonders bed_bath_table dominiert mit einem Anteil von rund 17 %."
                "Die Kategorie garden_tools ist bei schlechteren Anbietern kaum vorhanden."
                "Die schlechten Anbieter hingegen zeigen eine gleichmäßigere Verteilung. <br>"
                )
    st.markdown("**Dies könnte darauf hinweisen, dass erfolgreiche Anbieter stärker spezialisiert sind und in einer begrenzten Anzahl von Produktkategorien vertreten sind. Diesen Fokus weisen erfolglose Anbieter nicht auf.**")
    st.subheader("Lieferzeiten")
    fig = px.histogram(
    late_df,
    x="time_difference",
    color="review_score",
    barmode="stack",
    title="Review vs. Order", 
    )
    st.plotly_chart(fig)
    st.markdown("**Die Mehrheit der Bewertungen fällt negativ aus, wobei 2-Sterne-Bewertungen am häufigsten vorkommen. Positive Bewertungen sind in der Minderheit und verteilen sich über die Lieferzeit hinsichtlich der Anteile weniger**  \n"
                "Möglicherweise sind diese Produkt in Masse vorhanden, was für eine schlechtere Qualität (ergo schlechtere Bewertungen) sprechen könnte.")
    

elif auswahl == "8. Zusammenhänge der Variablen Lieferzeit, Versandkosten, Standorte":
    url = "https://drive.google.com/uc?export=download&id=1EOzTgetN3P5aibj9dXkBDsTLBAE_Nxbj"
    url_1 = "https://drive.google.com/uc?export=download&id=1D4w9a2uhAm1-ANC8w1V0KVanse4kLe9C"
    url_2 = "https://drive.google.com/uc?export=download&id=1YZARhhNH4xFhQljQP6bMdDkDJRpiML3F"
    
    df = pd.read_csv(url)
    df_2 = pd.read_csv(url_1)
    late_df = pd.read_csv(url_2)


    st.subheader("Wie hängen Größe und Gewicht eines Produkts oder Wert mit Versandkosten zusammen?")
    fig = sp.make_subplots(rows=1, cols=3, subplot_titles=(
    "Produktvolumen vs Versandkosten",
    "Produktgewicht vs Versandkosten",
    "Preis vs Versandkosten"
    ))
    fig1 = px.scatter(df, x="product_volume_cm3", y="freight_value", trendline="ols")
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    fig2 = px.scatter(df, x="product_weight_g", y="freight_value", trendline="ols")
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    fig3 = px.scatter(df, x="price", y="freight_value", trendline="ols")
    for trace in fig3.data:
        fig.add_trace(trace, row=1, col=3)
    
    fig.update_layout(
    title="Korrelationen mit Versandkosten",
    height=500,
    width=1200,
    showlegend=False
    )

    st.plotly_chart(fig)
    st.markdown("**Die Versandkosten zeigen bei allen 3 Variablen positive Zusammenhänge**. Allerdings ist es durch Ausreißer belastet, wenn man die Abbildungen mit den durchschnittlichen Kosten und Quartilen vergleicht.")

    st.subheader("Zusammenhang Lieferzeit und Entfernung")
    st.markdown("Die Entfernung (Distanz zwischen Kunde und Anbieter) wurde durch die Haversine Formel berechnet.")
    df_2_sample = df_2.sample(10000, random_state=42)
    fig = px.scatter(df_2_sample, x = "distance", y= "order_time_diff",opacity= 0.65,trendline = "ols",trendline_color_override= "red", range_y= [0,60],labels={"distance":"Distanz", "order_time_diff": "Versandzeit"})
    st.plotly_chart(fig)
    st.markdown("**Die beiden Variablen unterliegen einem positiven Zusammenhang**")
    st.subheader("Zusammenhang Versandkosten und Entfernung")
    st.markdown("Die Entfernung (Distanz zwischen Kunde und Anbieter) wurde durch die Haversine Formel berechnet.")
    df_2_sample = df_2.sample(10000, random_state=42)
    fig = px.scatter(df_2_sample, x = "freight_value", y= "distance",opacity= 0.65,trendline = "ols",trendline_color_override= "red", range_x=[0,150],labels={"distance":"Distanz", "freight_value": "Versandkosten"})
    st.plotly_chart(fig)
    st.markdown("**Die beiden Variablen unterliegen einem positiven Zusammenhang**")

    st.subheader("Analyse Verspäteter Bestellung")

    st.subheader("Allgemeine Verteilung der Verspätung (in Tagen)")
    fig = px.histogram(late_df, x = "time_difference", range_x=[0,100],labels={"time_difference":"Verspätung (in Tagen)", "count": "Anzahl"})
    fig.add_vline(x=8.87, line_width = 3, line_dash = "dash", line_color = "green", annotation_text = "Durchschnittliche Verspätung", annotation_position = "top right")
    st.plotly_chart(fig)
    st.markdown("50\% aller Bestellungen sind 5 Tage zu spät. Maximal kam ein Paket mit einer Verspätung von 188 Tagen zu spät.")
    st.subheader("Prozentuale Anteile der Versandzeit")
    fig = px.histogram(late_df, x = "time_percent", range_x=[0,100],labels={"time_percent":"Verspätung vom Lieferanten/Insgesamte Verspätung", "count": "Anzahl"})
    st.plotly_chart(fig)
    st.markdown("Der Prozentanteil bedeutet wie viel der Verspätung auf den Lieferanten zurückgeht. Ersichtlich ist eine linkschiefe Verteilung, was bedeutet das die Lieferanten größtenteils für die Verspätungen verantwortlich sind.  \n")
    st.markdown("**Die Lieferverzögerungen führen natürlich zu einer Unzufriedenheit der Kunden.**")
    st.markdown("Ein Vergleich der Distanz erfolgreicher und nicht erfolgreicher Bestellungen ergab:")
    st.markdown("**Die mittlere Lieferdistanz ist um 32\% höher als bei den erfolgreich gelieferten Bestellungen. Das ist ein möglicher Grund für die verspäteten Lieferungen. Und erklärt möglicherweise auch, wieso die Verspätungen zumeist von den Lieferanten ausgehen.**")
























