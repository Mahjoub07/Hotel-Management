import streamlit as st
import sqlite3
from datetime import date

# Connexion à la base SQLite
conn = sqlite3.connect("hotel.db")
c = conn.cursor()

st.title("Gestion Hôtelière")

# Menu de navigation
menu = ["Accueil", "Réservations", "Clients", "Chambres disponibles", "Ajouter un client", "Ajouter une réservation"]
choice = st.sidebar.selectbox("Menu", menu)

# 1. Liste des réservations
if choice == "Réservations":
    st.subheader("Liste des réservations")
    c.execute("""
        SELECT R.Id_Reservation, C.Nom_complet, R.Date_arrivee, R.Date_depart
        FROM Reservation R
        JOIN Client C ON R.Id_Client = C.Id_Client
    """)
    data = c.fetchall()
    st.table(data)

# 2. Liste des clients
elif choice == "Clients":
    st.subheader("Liste des clients")
    c.execute("SELECT * FROM Client")
    st.dataframe(c.fetchall())

# 3. Chambres disponibles
elif choice == "Chambres disponibles":
    st.subheader("Chambres disponibles")
    date_debut = st.date_input("Date d'arrivée", date(2025, 7, 1))
    date_fin = st.date_input("Date de départ", date(2025, 7, 10))

    if date_debut and date_fin:
        query = """
        SELECT * FROM Chambre
        WHERE Id_Chambre NOT IN (
            SELECT Co.Id_Chambre
            FROM Concerner Co
            JOIN Reservation R ON Co.Id_Reservation = R.Id_Reservation
            WHERE R.Date_arrivee <= ? AND R.Date_depart >= ?
        )
        """
        c.execute(query, (date_fin, date_debut))
        st.dataframe(c.fetchall())

# 4. Ajouter un client
elif choice == "Ajouter un client":
    st.subheader("Ajouter un nouveau client")
    with st.form("form_client"):
        nom = st.text_input("Nom complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        cp = st.number_input("Code postal", step=1)
        email = st.text_input("Email")
        tel = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter")

        if submitted:
            c.execute("SELECT MAX(Id_Client) + 1 FROM Client")
            next_id = c.fetchone()[0] or 1
            c.execute("INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (next_id, adresse, ville, cp, email, tel, nom))
            conn.commit()
            st.success("Client ajouté avec succès.")

# 5. Ajouter une réservation
elif choice == "Ajouter une réservation":
    st.subheader("Ajouter une réservation")
    with st.form("form_reservation"):
        c.execute("SELECT Id_Client, Nom_complet FROM Client")
        clients = c.fetchall()
        client_id = st.selectbox("Client", clients, format_func=lambda x: f"{x[1]} (ID: {x[0]})")

        date_arrivee = st.date_input("Date d'arrivée")
        date_depart = st.date_input("Date de départ")

        c.execute("SELECT Id_Chambre FROM Chambre")
        chambres = [row[0] for row in c.fetchall()]
        chambre_id = st.selectbox("Chambre", chambres)

        submitted = st.form_submit_button("Réserver")

        if submitted:
            c.execute("SELECT MAX(Id_Reservation) + 1 FROM Reservation")
            next_id = c.fetchone()[0] or 1
            c.execute("INSERT INTO Reservation VALUES (?, ?, ?, ?)",
                      (next_id, date_arrivee, date_depart, client_id[0]))
            c.execute("INSERT INTO Concerner VALUES (?, ?)", (next_id, chambre_id))
            conn.commit()
            st.success("Réservation enregistrée avec succès.")

# Accueil
else:
    st.markdown("Bienvenue dans l'application de gestion des réservations hôtelières.")
