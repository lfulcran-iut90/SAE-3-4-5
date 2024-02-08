DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS utilisateur;
DROP table if exists boisson;
DROP table if exists type_boisson;
DROP table if exists conditionnement;
DROP table if exists arome;




CREATE TABLE arome (
    id_arome INT PRIMARY KEY,
    nom_arome VARCHAR(255) NOT NULL
);


CREATE TABLE conditionnement (
    id_conditionnement INT PRIMARY KEY,
    nom_conditionnement VARCHAR(255) NOT NULL,
    prix DECIMAL(10, 2) NOT NULL
);

CREATE TABLE type_boisson (
    id_type_boisson INT PRIMARY KEY AUTO_INCREMENT,
    nom_type_boisson VARCHAR(255) NOT NULL
);

CREATE TABLE boisson (
    id_boisson INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL,
    prix DECIMAL(10, 2) NOT NULL,
    volume INT NOT NULL,
    arome_id INT,
    conditionnement_id INT,
    type_boisson_id INT,
    description TEXT,
    fournisseur VARCHAR(255),
    marque VARCHAR(255),
    stock INT NOT NULL,
    image VARCHAR(255),
    FOREIGN KEY (arome_id) REFERENCES arome(id_arome),
    FOREIGN KEY (conditionnement_id) REFERENCES conditionnement(id_conditionnement),
    FOREIGN KEY (type_boisson_id) REFERENCES type_boisson(id_type_boisson)
);
CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    nom VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_utilisateur)
);

CREATE TABLE adresse  (
    id_adresse INT AUTO_INCREMENT,
    nom_facturation VARCHAR(255) NOT NULL,
    rue VARCHAR(255) NOT NULL,
    code_postal INT NOT NULL,
    ville VARCHAR(255),
    utilisateur_id INT NOT NULL, 
    PRIMARY KEY(id_adresse),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE etat (
    id_etat INT AUTO_INCREMENT,
    libelle VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_etat)
);

CREATE TABLE commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATE NOT NULL,
    utilisateur_id INT,
    etat_id INT,
    adresse_id INT NOT NULL,
    PRIMARY KEY (id_commande),
    FOREIGN KEY fk_lb_r(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
    FOREIGN KEY (adresse_id) REFERENCES adresse(id_adresse)
);


CREATE TABLE ligne_commande (
    commande_id INT,
    boisson_id INT,
    prix DECIMAL(10, 2) NOT NULL,
    quantite INT NOT NULL,
    PRIMARY KEY (commande_id, boisson_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (boisson_id) REFERENCES boisson(id_boisson)
);

CREATE TABLE ligne_panier (
    utilisateur_id INT,
    boisson_id INT,
    quantite INT NOT NULL,
    date_ajout DATE,
    PRIMARY KEY (utilisateur_id, boisson_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (boisson_id) REFERENCES boisson(id_boisson)
);




INSERT INTO arome (id_arome, nom_arome) VALUES
(1, 'Vanille'),
(2, 'Fraise'),
(3, 'Citron'),
(4, 'Menthe'),
(5, 'Chocolat'),
(6, 'Amande'),
(7, 'Lait'),
(8, 'Nature'),
(9, 'Fruit Rouge'),
(10, 'Orange');


INSERT INTO conditionnement (id_conditionnement, nom_conditionnement, prix) VALUES
(1, 'Bouteille en verre', 1.5),
(2, 'Canette en aluminium', 0.8),
(3, 'Bouteille en plastique', 1.0);

INSERT INTO type_boisson (nom_type_boisson) VALUES
('Soda'),
('Jus de fruit'),
('Eau gazeuse'),
('Smoothie'),
('Eau plate'),
('Infusion'),
('Boisson énergisante'),
('Eau aromatisée');

INSERT INTO boisson (nom, prix, volume, arome_id, conditionnement_id, type_boisson_id, description, fournisseur, marque, stock, image) VALUES
('Soda à la vanille', 2.5, 500, 1, 1, 1, 'Boisson gazeuse à la vanille', 'ABC Company', 'SodaMaster',80, 'soda_vanille.jpg'),
('Jus de fraise', 3.0, 250, 2, 2, 2, 'Jus naturel de fraise', 'XYZ Juice Co.', 'FreshFruit',70, 'JusFraise.jpg'),
('Eau gazeuse citron', 1.0, 750, 3, 3, 3, 'Eau gazeuse au citron rafraîchissante', 'Aqua Ltd.','CitrusSplash',74, 'EauGazCitron.jpg'),
('Fraise-Banane Smoothie', 4.5, 400, 2, 1, 4, 'Smoothie rafraîchissant à la fraise et à la banane', 'SmoothieHeaven', 'BerryBanana',8, 'SmoothieFraiseBanane.jpg'),
('Eau de source naturelle', 0.75, 1000, 6, 3, 5, 'Eau pure et naturelle', 'SourcePure', 'ClearSpring', 15,'EauSource.jpg'),
('Camomille Infusion', 1.8, 250, 4, 1, 6, 'Infusion apaisante à la camomille', 'HerbalTeas', 'CalmingChamomile', 120,'CamomilleInfusion.jpg'),
('Limonade pétillante', 2.2, 500, 3, 2, 3, 'Limonade rafraîchissante et pétillante', 'FizzDrinks', 'SparkleLemonade', 70,'LimonadePetillante.jpg'),
('Boisson énergisante aux fruits rouges', 2.9, 330, 7, 2, 7, 'Boisson énergisante aux saveurs de fruits rouges', 'EnergyBoost', 'BerryCharge',77, 'BoissonFruitRouge.jpg'),
('Jus d\'orange frais pressé', 3.2, 300, 8, 1, 2, 'Jus d\'orange fraîchement pressé', 'CitrusHarvest', 'FreshSqueeze',111, 'Orange.jpg'),
('Eau aromatisée à la fraise', 1.5, 600, 2, 3, 8, 'Eau infusée à la fraise pour une saveur légère', 'FruitInfusions', 'StrawberrySplash',45, 'EauFraise.png'),
('Jus de pêche', 2.8, 350, 9, 1, 2, 'Jus naturel de pêche', 'FruitHarvest', 'PeachyDelight', 23,'JusPeche.jpg'),
('Eau aromatisée à la pomme', 1.4, 500, 10, 3, 8, 'Eau infusée à la pomme pour une saveur fruitée', 'FruitInfusions', 'AppleBurst', 25,'EauPomme.png'),
('Smoothie pomme-kiwi', 4.0, 450, 4, 3, 4, 'Smoothie rafraîchissant à la pomme et au kiwi', 'SmoothieHeaven', 'MintyFresh', 65,'SmoothiePommeKiwi.jpg'),
('Soda à l\'orange', 2.3, 500, 8, 2, 1, 'Boisson gazeuse à l\'orange pétillante', 'ABC Company', 'OrangeFizz', 62,'SodaOrange.jpg'),
('Infusion de fruits rouges', 1.7, 300, 7, 1, 6, 'Infusion délicieuse de fruits rouges', 'HerbalTeas', 'BerryInfusion', 98,'InfusionFruitRouge.jpg'),
('Jus de pomme', 2.0, 300, 10, 3, 2, 'Jus naturel de pomme', 'FruitHarvest', 'AppleFresh', 12,'JusPomme.jpg'),
('Eau gazeuse à la menthe', 1.2, 500, 4, 3, 3, 'Eau gazeuse à la menthe rafraîchissante', 'Aqua Ltd.', 'MintSplash', 63,'EauGazMenthe.jpg'),
('Jus aux fruits rouges', 2.0, 300, 4, 3, 2, 'Jus naturel à la framboise, aux cassis avec une touche de pommes', 'XYZ Juice Co.', 'CoolMintJuice', 98,'JusFruitsRouges.jpg'),
('Boisson énergisante menthe-citron', 3.5, 330, 4, 2, 7, 'Boisson énergisante revigorante à l\'arôme de menthe et aux citrons', 'EnergyBoost', 'MintEnergy', 45,'BoissonEnergisanteMentheCitron.jpg');


INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2');

INSERT INTO adresse (nom_facturation, rue, code_postal, ville, utilisateur_id) VALUES
('Facturation Client 1', '123 Main Street', 12345, 'City1', 2),
('Facturation Client 2', '456 Oak Avenue', 56789, 'City2', 2),
('Facturation Client 3', '789 Pine Lane', 90123, 'City3', 2),
('Facturation Client2 1', '111 Elm Street', 11111, 'CityA', 3),
('Facturation Client2 2', '222 Maple Avenue', 22222, 'CityB', 3),
('Facturation Client2 3', '333 Cedar Lane', 33333, 'CityC', 3);


INSERT INTO etat (libelle) VALUES
('En attente'),
('En cours de traitement'),
('Expédiée'),
('Annulée');







SELECT *
FROM ligne_panier;


SELECT SUM(b.prix * quantite)
FROM ligne_panier
LEFT JOIN boisson b on ligne_panier.boisson_id = b.id_boisson;

SELECT id_utilisateur
FROM utilisateur
WHERE login = 'admin' AND email = 'admin@admin.fr';