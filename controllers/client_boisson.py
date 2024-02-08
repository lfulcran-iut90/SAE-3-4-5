#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_boisson = Blueprint('client_boisson', __name__,
                        template_folder='templates')

@client_boisson.route('/client/index')
@client_boisson.route('/client/boisson/show')              # remplace /client
def client_boisson_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''   selection des boissons   '''
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''

    sql = '''SELECT *
            FROM boisson;'''
    mycursor.execute(sql)
    boissons = mycursor.fetchall()


    # pour le filtre
    sql = '''SELECT *
             FROM type_boisson;'''
    mycursor.execute(sql)
    types_boisson = mycursor.fetchall()

    tuple = (id_client,)
    sql= '''SELECT boisson.id_boisson,boisson.nom, ligne_panier.quantite, boisson.prix, boisson.stock
            FROM ligne_panier
            LEFT JOIN boisson ON boisson.id_boisson = ligne_panier.boisson_id
            WHERE utilisateur_id = %s;
            '''
    mycursor.execute(sql, tuple)
    boissons_panier = mycursor.fetchall()

    if len(boissons_panier) >= 1:
        sql = ''' SELECT SUM(b.prix * quantite)
                  FROM ligne_panier
                  LEFT JOIN boisson b on ligne_panier.boisson_id = b.id_boisson; '''
        mycursor.execute(sql)
        prix_total = mycursor.fetchone()
    else:
        prix_total = None
    return render_template('client/boutique/panier_boisson.html'
                           , boissons=boissons
                           , boissons_panier=boissons_panier
                           #, prix_total=prix_total
                           , items_filtre=types_boisson
                           )
