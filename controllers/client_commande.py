#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_utilisateur = (id_client,)

    sql = '''
            SELECT utilisateur_id, boisson_id, quantite, date_ajout, id_boisson, nom, prix
            FROM ligne_panier
            LEFT JOIN boisson b on b.id_boisson = ligne_panier.boisson_id
            WHERE utilisateur_id = %s;
    '''
    mycursor.execute(sql, id_utilisateur)
    boissons_panier = mycursor.fetchall()

    if len(boissons_panier) >= 1:
        sql = '''
            SELECT SUM(b.prix * quantite) AS prix_total
            FROM ligne_panier
            LEFT JOIN boisson b on ligne_panier.boisson_id = b.id_boisson
            WHERE utilisateur_id = %s; '''
        mycursor.execute(sql, id_utilisateur)
        temp = mycursor.fetchone()
        prix_total = temp['prix_total']
    else:
        prix_total = 0
        
    
    sql = '''
            SELECT *
            FROM adresse
            WHERE utilisateur_id = %s;
          '''
    mycursor.execute(sql, id_utilisateur)
    adresses = mycursor.fetchall()
    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , boissons_panier=boissons_panier
                           , prix_total=prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    id_adresse_livraison = request.form.get('id_adresse_livraison')
    id_adresse_facturation = request.form.get('id_adresse_facturation')

    id_client = session['id_user']

    id_utilisateur = (id_client,)
    sql = '''
            SELECT utilisateur_id, boisson_id, quantite, date_ajout, b.prix
            FROM ligne_panier
            LEFT JOIN boisson b on b.id_boisson = ligne_panier.boisson_id
            WHERE utilisateur_id = %s;'''
    mycursor.execute(sql, id_utilisateur)
    items_ligne_panier = mycursor.fetchall()

    if items_ligne_panier is None or len(items_ligne_panier) < 1:
         flash(u'Pas d\'boissons dans le ligne_panier', 'alert-warning')
         return redirect('/client/boisson/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")
    commande = (id_client,id_adresse_livraison,id_adresse_facturation)

    #Porblème id_livraison
    sql = ''' 
    INSERT INTO commande(date_achat,utilisateur_id, etat_id, adresse_livraison,adresse_facturation) VALUES
        (NOW(), %s, 1, %s, %s);
    '''
    mycursor.execute(sql, commande)
    get_db().commit()

    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    last_insert_id = mycursor.fetchone()
    last_insert_id = last_insert_id['last_insert_id']

    # numéro de la dernière commande
    for item in items_ligne_panier:
        id_boisson = item['boisson_id']
        prix_boisson = item['prix']
        quantité = item['quantite']
        ligne_panier = (id_boisson, id_client)
        sql = ''' DELETE
                  FROM ligne_panier
                  WHERE boisson_id = %s AND utilisateur_id = %s'''
        mycursor.execute(sql, ligne_panier)

        print(last_insert_id, id_boisson,prix_boisson,quantité)
        tuple_commande = (last_insert_id, id_boisson,prix_boisson,quantité)
        sql = '''
        INSERT INTO ligne_commande(commande_id, boisson_id, prix, quantite) VALUES
            (%s,%s,%s,%s);
        '''
        mycursor.execute(sql, tuple_commande)

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/boisson/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    tuple = (id_client,)
    sql = '''  
            SELECT id_commande,date_achat,utilisateur_id, e.libelle, SUM(lc.prix * lc.quantite) AS prix_total , etat_id, SUM(quantite) AS nbr_boissons
            FROM commande
            LEFT JOIN ligne_commande lc on commande.id_commande = lc.commande_id
            LEFT JOIN etat e on e.id_etat = commande.etat_id
            WHERE commande.utilisateur_id = %s
            GROUP BY id_commande
            ORDER BY date_achat DESC;
          '''
    mycursor.execute(sql, tuple)
    commandes = mycursor.fetchall()

    boissons_commande = []
    commande_adresses = []

    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        tuple = (id_client, id_commande)
        sql = '''
                SELECT id_commande, b.prix as prix, lc.prix*lc.quantite as prix_ligne,quantite,b.nom
                FROM commande
                LEFT JOIN ligne_commande lc on commande.id_commande = lc.commande_id
                LEFT JOIN boisson b on lc.boisson_id = b.id_boisson
                WHERE commande.utilisateur_id = %s AND id_commande = %s;
            '''
        mycursor.execute(sql, tuple)
        boissons_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' SELECT a.nom_facturation, a.rue AS rue_facturation, a.ville AS ville_facturation, a.code_postal AS code_postal_facturation,
                       a2.nom_facturation as nom_livraison, a2.rue AS rue_livraison, a2.ville AS ville_livraison, a2.code_postal AS code_postal_livraison
                FROM commande
                LEFT JOIN adresse a on a.id_adresse = commande.adresse_facturation
                LEFT JOIN adresse a2 on a2.id_adresse = commande.adresse_livraison
                WHERE commande.utilisateur_id = %s AND id_commande = %s;
                '''

        mycursor.execute(sql, tuple)
        commande_adresses = mycursor.fetchone()

        if commande_adresses['nom_facturation'] == commande_adresses['nom_livraison'] and commande_adresses['rue_facturation'] == commande_adresses['rue_livraison'] and commande_adresses['ville_facturation'] == commande_adresses['ville_livraison'] and commande_adresses['code_postal_facturation'] == commande_adresses['code_postal_livraison'] :
            commande_adresses['adresse_identique'] = 'adresse_identique'

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , boissons_commande=boissons_commande
                           , commande_adresses=commande_adresses
                           )

