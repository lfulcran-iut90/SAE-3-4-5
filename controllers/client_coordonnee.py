#! /usr/bin/python
# -*- coding:utf-8 -*-
import code
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    tuple = (id_client,)

    sql = '''SELECT login, email,nom
             FROM utilisateur
             WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, tuple)
    utilisateur = mycursor.fetchone()

    sql = '''
            SELECT *
            FROM adresse
            WHERE utilisateur_id = %s;'''
    mycursor.execute(sql, tuple)
    adresses = mycursor.fetchall()

    sql = '''SELECT COUNT(id_adresse) AS nb_adresses
             FROM adresse
             WHERE utilisateur_id = %s;'''
    mycursor.execute(sql, tuple)
    temp = mycursor.fetchone()
    nb_adresses = temp['nb_adresses']

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                           , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    tuple = (id_client,)
    sql = '''SELECT login, email,nom
             FROM utilisateur
             WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, tuple)
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    tuple = (email, nom, id_client)
    sql = '''SELECT *
             FROM utilisateur
             WHERE (email = %s OR nom = %s) AND id_utilisateur != %s;'''
    mycursor.execute(sql, tuple)
    utilisateur = mycursor.fetchall()

    if utilisateur:
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                                , utilisateur = utilisateur
                               )

    tuple = (nom, login, email, id_client)
    sql = '''UPDATE utilisateur
             SET nom = %s, login = %s, email = %s
             WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, tuple)
    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')
    print(id_adresse, id_client)

    tuple = (id_client,id_adresse,id_adresse)
    sql = '''
            SELECT *
            FROM commande
            WHERE utilisateur_id = %s AND (adresse_livraison = %s OR adresse_facturation = %s)'''
    mycursor.execute(sql, tuple)
    commande_utile = mycursor.fetchone()

    print(commande_utile)
    tuple = (id_adresse,)
    if commande_utile :
        sql = '''
                UPDATE adresse
                SET valide = false
                WHERE id_adresse = %s;
            '''
        mycursor.execute(sql, tuple)
        flash(u'cette adresse est utilisée dans une(des) commande(s) : vous ne pouvez pas la supprimer ; cependant cette adresse ne sera plus utilisable'
              , 'alert-warning')
    else:
        sql  = '''
                DELETE
                FROM adresse
                WHERE id_adresse = %s;
                '''
        mycursor.execute(sql,tuple)

    get_db().commit()
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    tuple = (id_client,)
    sql = '''SELECT login, nom
             FROM utilisateur
             WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, tuple)
    utilisateur = mycursor.fetchone()


    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    tuple = (nom, rue, code_postal, ville, id_client)
    sql = '''
        INSERT INTO adresse (nom_facturation, rue, code_postal, ville, utilisateur_id) VALUES
        (%s,%s,%s,%s,%s)'''
    mycursor.execute(sql, tuple)
    get_db().commit()
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    tuple = (id_client,)
    sql = '''SELECT login, nom
             FROM utilisateur
             WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, tuple)
    utilisateur = mycursor.fetchone()

    tuple = (id_adresse,)
    sql = '''SELECT *
             FROM adresse
             WHERE id_adresse = %s;'''
    mycursor.execute(sql, tuple)
    adresse = mycursor.fetchone()
    print(adresse)

    return render_template('/client/coordonnee/edit_adresse.html'
                            ,utilisateur=utilisateur
                            ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    tuple = (nom, rue, code_postal,ville,id_adresse)
    sql = '''UPDATE adresse
             SET nom_facturation = %s, rue =%s, code_postal =%s, ville = %s
             WHERE id_adresse = %s;'''
    mycursor.execute(sql, tuple)
    get_db().commit()

    return redirect('/client/coordonnee/show')
