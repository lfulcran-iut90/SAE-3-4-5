#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_boisson=request.form.get('id_declinaison_boisson',None)
    id_declinaison_boisson = 1

# ajout dans le panier d'une déclinaison d'un boisson (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_boisson))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_boisson = declinaisons[0]['id_declinaison_boisson']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_boisson))
    #     boisson = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_boisson.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , boisson=boisson)

    tuple =(id_boisson, id_client)
    sql = '''SELECT boisson_id
             FROM ligne_panier
             WHERE boisson_id = %s AND utilisateur_id = %s;'''
    mycursor.execute(sql, tuple)
    boissonPresent = mycursor.fetchone()

    if boissonPresent is None:
        tuple = (id_client, id_boisson, quantite)
        sql = '''INSERT INTO ligne_panier(utilisateur_id, boisson_id, quantite,date_ajout) VALUES 
            (%s, %s, %s, NOW()) ;'''
        mycursor.execute(sql, tuple)
        get_db().commit()
    else:
        tuple = (quantite, id_boisson)
        sql = '''UPDATE ligne_panier
          SET quantite = quantite + %s
          WHERE boisson_id = %s;'''
        mycursor.execute(sql, tuple)
        get_db().commit()


    tuple = (quantite, id_boisson)
    sql = '''UPDATE boisson
    SET stock = stock - %s
    WHERE id_boisson = %s;'''
    mycursor.execute(sql, tuple)
    get_db().commit()



    return redirect('/client/boisson/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'boisson
    # id_declinaison_boisson = request.form.get('id_declinaison_boisson', None)

    tuple = (id_boisson)
    sql = ''' SELECT *
              FROM ligne_panier
              WHERE boisson_id = %s'''
    mycursor.execute(sql, tuple)
    boisson_panier=mycursor.fetchone()


    if not(boisson_panier is None) and boisson_panier['quantite'] > 1:
        sql = ''' UPDATE ligne_panier
                  SET quantite = quantite - 1;'''
        mycursor.execute(sql)

    else:
        tuple = (id_boisson, id_client)
        sql = ''' DELETE FROM ligne_panier
                  WHERE boisson_id = %s AND utilisateur_id = %s;'''
        mycursor.execute(sql, tuple)

    tuple = (id_boisson,)
    sql = ''' UPDATE boisson
              SET stock = stock + 1
              WHERE id_boisson = %s;'''
    mycursor.execute(sql, tuple)
    get_db().commit()
    return redirect('/client/boisson/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''SELECT *
             FROM ligne_panier;'''
    mycursor.execute(sql)
    items_panier = mycursor.fetchall()

    for item in items_panier:
        tuple = (client_id)
        sql = ''' DELETE FROM ligne_panier
                  WHERE utilisateur_id = %s;'''
        mycursor.execute(sql, tuple)

        tuple = (item['quantite'], item['boisson_id'])
        sql2='''UPDATE boisson
                SET stock = stock + %s
                WHERE id_boisson = %s;'''
        mycursor.execute(sql2, tuple)
        get_db().commit()
    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson')
    #id_declinaison_boisson = request.form.get('id_declinaison_boisson')

    tuple = (id_boisson, id_client)
    sql = ''' SELECT *
              FROM ligne_panier
              WHERE boisson_id = %s and utilisateur_id = %s;'''
    mycursor.execute(sql, tuple)
    boisson_panier = mycursor.fetchone()

    tuple = (id_client, id_boisson)
    sql = '''DELETE FROM ligne_panier
             WHERE utilisateur_id = %s and boisson_id = %s;'''
    mycursor.execute(sql, tuple)


    tuple = (boisson_panier['quantite'], id_boisson)
    sql2='''UPDATE boisson
            SET stock = stock + %s
            WHERE id_boisson = %s;'''
    mycursor.execute(sql2, tuple)

    get_db().commit()
    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    mycursor = get_db().cursor()

    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    temp = []


    sql = '''SELECT *
             FROM type_boisson;'''
    mycursor.execute(sql)
    type_boisson = mycursor.fetchall()

    if filter_word and filter_word != "":
        if filter_prix_min or filter_prix_max:
            if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
                if int(filter_prix_min) < int(filter_prix_max):
                    if filter_types and filter_types != []:
                        for case in filter_types:
                            tuple = (case, filter_prix_min, filter_prix_max, f"%{filter_word}%")
                            sql = ''' SELECT *
                                      FROM boisson
                                      WHERE type_boisson_id =%s AND prix BETWEEN %s AND %s AND nom LIKE %s;'''
                            mycursor.execute(sql, tuple)
                            boisson = mycursor.fetchall()
                            if len(boisson) > 0:
                                temp = temp + boisson
                        session['filter_word'] = filter_word
                        session['filter_prix_min'] = filter_prix_min
                        session['filter_prix_max'] = filter_prix_max
                        session['filter_types'] = filter_types
                        get_db().commit()
                        return render_template('client/boutique/panier_boisson.html', boissons=temp,
                                               items_filtre=type_boisson)
                    else:

                        tuple = (f"%{filter_word}%", filter_prix_min, filter_prix_max)
                        sql = ''' SELECT *
                                      FROM boisson
                                      WHERE prix BETWEEN %s AND %s AND nom LIKE %s;'''
                        mycursor.execute(sql, tuple)
                        boisson = mycursor.fetchall()
                        session['filter_word'] = filter_word
                        session['filter_prix_min'] = filter_prix_min
                        session['filter_prix_max'] = filter_prix_max
                        get_db().commit()
                        return render_template('client/boutique/panier_boisson.html', boissons=boisson,
                                               items_filtre=type_boisson)
        else:
            if filter_types and filter_types != []:
                for case in filter_types:
                    tuple = (case, f"%{filter_word}%")
                    sql = '''SELECT *
                                 FROM boisson
                                 WHERE type_boisson_id =%s AND nom LIKE %s;'''
                    mycursor.execute(sql, tuple)
                    boisson = mycursor.fetchall()
                    if len(boisson) > 0:
                        temp = temp + boisson
                session['filter_word'] = filter_word
                session['filter_types'] = filter_types
                get_db().commit()
                return render_template('client/boutique/panier_boisson.html', boissons=temp,
                                       items_filtre=type_boisson)
            else:
                tuple = (f"%{filter_word}%")
                sql = '''SELECT *
                         FROM boisson
                         WHERE nom LIKE %s;'''
                mycursor.execute(sql, tuple)
                boisson = mycursor.fetchall()
                session['filter_word'] = filter_word
                get_db().commit()
                return render_template('client/boutique/panier_boisson.html', boissons=boisson,
                                       items_filtre=type_boisson)

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                if filter_types and filter_types != []:
                    for case in filter_types:
                        tuple = (case, filter_prix_min, filter_prix_max)
                        sql = ''' SELECT *
                                      FROM boisson
                                      WHERE type_boisson_id =%s AND prix BETWEEN %s AND %s;'''
                        mycursor.execute(sql, tuple)
                        boisson = mycursor.fetchall()
                        if len(boisson) > 0:
                            temp = temp + boisson
                    session['filter_prix_min'] = filter_prix_min
                    session['filter_prix_max'] = filter_prix_max
                    session['filter_types'] = filter_types
                    get_db().commit()
                    return render_template('client/boutique/panier_boisson.html', boissons=temp,
                                           items_filtre=type_boisson)

                else:
                    tuple = (filter_prix_min, filter_prix_max)
                    sql = '''SELECT *
                                 FROM boisson
                                 WHERE prix BETWEEN %s AND %s;'''
                    mycursor.execute(sql, tuple)
                    boisson = mycursor.fetchall()
                    session['filter_prix_min'] = filter_prix_min
                    session['filter_prix_max'] = filter_prix_max
                    get_db().commit()
                    return render_template('client/boutique/panier_boisson.html', boissons=boisson,
                                           items_filtre=type_boisson)

    if filter_types and filter_types != []:
        for case in filter_types:
            tuple = (case,)
            sql = ''' SELECT *
                      FROM boisson
                      WHERE type_boisson_id = %s;'''
            mycursor.execute(sql, tuple)
            boisson = mycursor.fetchall()
            if len(boisson) > 0:
                temp = temp + boisson
        session['filter_types'] = filter_types
        get_db().commit()
        return render_template('client/boutique/panier_boisson.html', boissons=temp, items_filtre=type_boisson)

    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():

    if 'filter_word' in session:
        session.pop('filter_word')
    if 'filter_prix_min' in session:
        session.pop('filter_prix_min')
    if 'filter_prix_max' in session:
        session.pop('filter_prix_max')
    if 'filter_types' in session:
        session.pop('filter_types')
    return redirect('/client/boisson/show')

