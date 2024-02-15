#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
# from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_boisson = Blueprint('admin_boisson', __name__,
                          template_folder='templates')


@admin_boisson.route('/admin/boisson/show')
def show_boisson():
    mycursor = get_db().cursor()
    sql = '''  SELECT * FROM boisson
    LEFT JOIN arome a on boisson.arome_id = a.id_arome
    LEFT JOIN type_boisson tb on boisson.type_boisson_id = tb.id_type_boisson
    '''
    mycursor.execute(sql)
    boissons = mycursor.fetchall()
    return render_template('admin/boisson/show_boisson.html', boissons=boissons)


@admin_boisson.route('/admin/boisson/add', methods=['GET'])
def add_boisson():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM type_boisson
    '''
    mycursor.execute(sql)
    type_boisson = mycursor.fetchall()
    sql = '''SELECT * FROM arome
    '''
    mycursor.execute(sql)
    arome = mycursor.fetchall()

    return render_template('admin/boisson/add_boisson.html',
                           types_boisson=type_boisson
                           ,arome=arome
                           # ,tailles=tailles
                           )


@admin_boisson.route('/admin/boisson/add', methods=['POST'])
def valid_add_boisson():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_boisson_id = request.form.get('type_boisson_id', '')
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    volume = request.form.get('volume', '')
    image = request.files.get('image', '')
    arome_id = request.form.get('arome_id', '')


    if image:
        filename = 'img_upload' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename = None

    sql = ''' INSERT INTO boisson (nom, prix, type_boisson_id, stock, volume, arome_id, image) VALUES (%s, %s, %s,%s, %s, %s, %s)
    '''

    tuple_add = (nom, prix, type_boisson_id, stock, volume, arome_id, filename)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'boisson ajouté , nom: ', nom, ' - type_boisson:', type_boisson_id, ' - prix:', prix,
          ' - stock:', stock, ' - image:', image, ' - volume:', volume)
    message = u'boisson ajouté , nom : ' + nom + '- type_boisson : ' + type_boisson_id + ' - prix : ' + prix + ' - stock : ' + stock + '- volume : ' + volume + ', arome : ' + arome_id + ', image : ' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/boisson/show')


@admin_boisson.route('/admin/boisson/delete', methods=['GET'])
def delete_boisson():
    id_boisson = request.args.get('id_boisson')
    mycursor = get_db().cursor()
    # sql = ''' SELECT * FROM boisson ---> PARTIE DECLINAISON GL LUCAS FULCRAND
    # '''
    # mycursor.execute(sql, id_boisson)
    # nb_declinaison = mycursor.fetchone()
    # if nb_declinaison['nb_declinaison'] > 0:
    #     message= u'il y a des declinaisons dans cet boisson : vous ne pouvez pas le supprimer'
    #     flash(message, 'alert-warning')
    # else:
    sql = ''' SELECT * FROM boisson WHERE id_boisson = %s '''
    mycursor.execute(sql, id_boisson)
    boisson = mycursor.fetchone()
    print(boisson)
    image = boisson['image']

    sql = ''' DELETE FROM commentaire WHERE id_boisson = %s  '''
    mycursor.execute(sql, id_boisson)
    get_db().commit()
    sql = ''' DELETE FROM historique WHERE id_boisson = %s  '''
    mycursor.execute(sql, id_boisson)
    get_db().commit()
    sql = ''' DELETE FROM liste_envie WHERE id_boisson = %s  '''
    mycursor.execute(sql, id_boisson)
    get_db().commit()
    sql = ''' DELETE FROM ligne_panier WHERE boisson_id = %s  '''
    mycursor.execute(sql, id_boisson)
    get_db().commit()
    sql = ''' DELETE FROM ligne_commande WHERE boisson_id = %s  '''
    mycursor.execute(sql, id_boisson)
    get_db().commit()
    sql = ''' DELETE FROM boisson WHERE id_boisson = %s  '''
    mycursor.execute(sql, id_boisson)
    get_db().commit()
    if image != None:
        os.remove('static/images/' + image)

    print("un boisson supprimé, id :", id_boisson)
    message = u'un boisson supprimé, id : ' + id_boisson
    flash(message, 'alert-success')


    return redirect('/admin/boisson/show')


@admin_boisson.route('/admin/boisson/edit', methods=['GET'])
def edit_boisson():
    id_boisson = request.args.get('id_boisson')
    mycursor = get_db().cursor()
    sql = '''
    SELECT * FROM boisson WHERE id_boisson =%s
    '''
    mycursor.execute(sql, id_boisson)
    boisson = mycursor.fetchone()
    print(boisson)
    sql = '''
    SELECT * FROM type_boisson
    '''
    mycursor.execute(sql)
    types_boisson = mycursor.fetchall()

    sql = '''
    SELECT * FROM arome
    '''
    mycursor.execute(sql)
    arome = mycursor.fetchall()

    # sql = '''
    # requête admin_boisson_6
    # '''
    # mycursor.execute(sql, id_boisson)
    # declinaisons_boisson = mycursor.fetchall()

    return render_template('admin/boisson/edit_boisson.html'
                           , boisson=boisson
                           , types_boisson=types_boisson
                           , arome=arome
                           #  ,declinaisons_boisson=declinaisons_boisson
                           )


@admin_boisson.route('/admin/boisson/edit', methods=['POST'])
def valid_edit_boisson():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_boisson = request.form.get('id_boisson')
    image = request.files.get('image', '')
    type_boisson_id = request.form.get('type_boisson_id', '')
    prix = request.form.get('prix', '')
    stock = request.form.get('stock')
    volume = request.form.get('volume')
    arome_id = request.form.get('arome_id', '')
    sql = '''SELECT image from boisson WHERE id_boisson = %s'''
    mycursor.execute(sql, id_boisson)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename
    tuple_update = (nom, type_boisson_id, prix, stock, volume, arome_id, image_nom, id_boisson)
    sql = '''
       UPDATE boisson SET nom =%s, type_boisson_id =%s, prix =%s, stock =%s, volume =%s, arome_id =%s, image = %s where id_boisson =%s
       '''
    mycursor.execute(sql, tuple_update)

    # sql = '''  requête admin_boisson_9 '''
    # mycursor.execute(sql, (nom, image_nom, prix, type_boisson_id, description, id_boisson))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'boisson modifié , nom:' + nom + '- type_boisson :' + type_boisson_id + ' - prix:' + prix + ' - image:' + image_nom + ' - stock: ' + stock + ' volume : ' + volume + ', arome : ' + arome_id
    flash(message, 'alert-success')
    return redirect('/admin/boisson/show')


@admin_boisson.route('/admin/boisson/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    boisson = []
    commentaires = {}
    return render_template('admin/boisson/show_avis.html'
                           , boisson=boisson
                           , commentaires=commentaires
                           )


@admin_boisson.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    boisson_id = request.form.get('idboisson', None)
    userId = request.form.get('idUser', None)

    return admin_avis(boisson_id)
