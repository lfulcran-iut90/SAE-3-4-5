#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_liste_envies = Blueprint('client_liste_envies', __name__,
                        template_folder='templates')


@client_liste_envies.route('/client/envie/add', methods=['get'])
def client_liste_envies_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.args.get('id_boisson')
    liste_envie = (id_client, id_boisson)

    sql =  '''
            SELECT *
            FROM liste_envie
            WHERE id_utilisateur = %s AND id_boisson = %s;
          '''
    mycursor.execute(sql, liste_envie)
    present = mycursor.fetchall()

    if present :
        flash(u'Cette boisson est déjà dans votre liest d\'envie', 'alert-warning')
        return redirect('/client/boisson/show')

    sql = '''
            INSERT INTO liste_envie(id_utilisateur,id_boisson) VALUES 
            (%s,%s);
            '''
    mycursor.execute(sql, liste_envie)
    get_db().commit()
    return redirect('/client/boisson/show')




@client_liste_envies.route('/client/envie/delete', methods=['get'])
def client_liste_envies_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.args.get('id_boisson')
    liste_envie = (id_client, id_boisson)

    sql = '''
            DELETE
            FROM liste_envie
            WHERE id_utilisateur = %s AND id_boisson = %s;
         '''
    mycursor.execute(sql, liste_envie)
    get_db().commit()

    return redirect('/client/envies/show')

@client_liste_envies.route('/client/envies/show', methods=['get'])
def client_liste_envies_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_utilisateur = (id_client)
    print(id_client)

    sql = '''
            SELECT liste_envie.id_boisson, id_utilisateur, b.id_boisson, b.nom, stock, prix, image
            FROM liste_envie
            LEFT JOIN boisson b on b.id_boisson = liste_envie.id_boisson
            WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, id_utilisateur)
    boissons_liste_envies = mycursor.fetchall()

    sql = '''
            SELECT historique.id_boisson, id_utilisateur, b.id_boisson, b.nom, prix, image
            FROM historique
            LEFT JOIN boisson b on b.id_boisson = historique.id_boisson
            WHERE id_utilisateur = %s
            ORDER  BY colonne_ordre;
            '''
    mycursor.execute(sql, id_utilisateur)
    boissons_historique = mycursor.fetchall()
    nb_liste_envies = len(boissons_liste_envies)

    return render_template('client/liste_envies/liste_envies_show.html'
                           ,boissons_liste_envies=boissons_liste_envies
                           , boissons_historique=boissons_historique
                           , nb_liste_envies= nb_liste_envies
                           )



def client_historique_add(article_id, client_id):
    mycursor = get_db().cursor()
    client_id = session['id_user']

    #Regarde si la boisson est dans l'historique
    sql ='''
            SELECT *
            FROM historique
            WHERE id_boisson = %s AND id_utilisateur = %s;
            '''
    mycursor.execute(sql, (article_id, client_id))
    historique_produit = mycursor.fetchone()



    if historique_produit:
        ordre = historique_produit['colonne_ordre']
        #Si oui replace la boisson au début de l'historique
        sql = '''
                    UPDATE historique
                    SET colonne_ordre = colonne_ordre + 1
                    WHERE colonne_ordre < %s;'''
        mycursor.execute(sql, (ordre,))

        sql = '''
                UPDATE historique
                SET colonne_ordre = 1
                WHERE id_boisson = %s AND id_utilisateur = %s;'''
        mycursor.execute(sql, (article_id, client_id))
        get_db().commit()
    #Sinon on la place dedans
    else:
        sql = '''
                UPDATE historique
                SET colonne_ordre = colonne_ordre + 1;'''
        mycursor.execute(sql)
        sql = '''
                INSERT INTO historique(id_boisson,id_utilisateur,colonne_ordre) VALUES 
                (%s, %s, 1);'''
        mycursor.execute(sql, (article_id, client_id))
        get_db().commit()


    sql ='''
            SELECT *
            FROM historique
            WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, (client_id))
    historiques = mycursor.fetchall()
    if len(historiques)>6:
        sql = '''
                DELETE
                FROM historique
                WHERE colonne_ordre > 6;'''
        mycursor.execute(sql)
        get_db().commit()



@client_liste_envies.route('/client/envies/up', methods=['get'])
@client_liste_envies.route('/client/envies/down', methods=['get'])
@client_liste_envies.route('/client/envies/last', methods=['get'])
@client_liste_envies.route('/client/envies/first', methods=['get'])
def client_liste_envies_boisson_move():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.args.get('id_boisson')
  
    return redirect('/client/envies/show')
