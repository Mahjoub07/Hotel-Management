USE HotelDB;

SELECT 
    R.Id_Reservation,
    C.Nom_complet,
    H.Ville AS Ville_Hotel
FROM 
    Reservation R
JOIN Client C ON R.Id_Client = C.Id_Client
JOIN Chambre Ch ON R.Id_Reservation = Ch.Id_Chambre 
JOIN Hotel H ON Ch.Id_Hotel = H.Id_Hotel;
-- b. Clients qui habitent à Paris
SELECT * 
FROM Client 
WHERE Ville = 'Paris';

-- c. Nombre de réservations faites par chaque client
SELECT 
    C.Nom_complet,
    COUNT(R.Id_Reservation) AS Nombre_Reservations
FROM 
    Client C
LEFT JOIN Reservation R ON C.Id_Client = R.Id_Client
GROUP BY C.Id_Client;

-- d. Nombre de chambres pour chaque type de chambre
SELECT 
    T.Type,
    COUNT(Ch.Id_Chambre) AS Nombre_Chambres
FROM 
    Type_Chambre T
LEFT JOIN Chambre Ch ON T.Id_Type = Ch.Id_Type
GROUP BY T.Type;

-- e. Chambres non réservées pour une période donnée

SET @date_debut = '2025-07-01';
SET @date_fin = '2025-07-10';

SELECT *
FROM Chambre Ch
WHERE Ch.Id_Chambre NOT IN (
    SELECT Co.Id_Chambre
    FROM Concerner Co
    JOIN Reservation R ON Co.Id_Reservation = R.Id_Reservation
    WHERE R.Date_arrivee <= @date_fin AND R.Date_depart >= @date_debut
);
