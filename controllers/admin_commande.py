#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                           template_folder='templates')


@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    id_commande = request.args.get('id_commande', None)
    sql = '''SELECT c.id_commande, u.login, c.date_achat, SUM(lc.quantite) AS nbr_boissons, ROUND(SUM(lc.prix * lc.quantite),2) AS prix_total, e.libelle, c.etat_id
    FROM commande c 
    INNER JOIN utilisateur u ON c.utilisateur_id = u.id_utilisateur
    INNER JOIN etat e ON c.etat_id = e.id_etat
    INNER JOIN ligne_commande lc on c.id_commande = lc.commande_id
    GROUP BY id_commande'''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()
    boissons_commande = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        sql = '''
                SELECT id_commande, b.prix as prix, lc.prix*lc.quantite as prix_total,quantite as nbr_boisson,b.nom
                FROM commande
                LEFT JOIN ligne_commande lc on commande.id_commande = lc.commande_id
                LEFT JOIN boisson b on lc.boisson_id = b.id_boisson
                WHERE id_commande=%s;
    '''
        mycursor.execute(sql, (id_commande,))
        boissons_commande = mycursor.fetchall()
    commande_adresses = None
    # print(id_commande)
    if id_commande != None:
        sql = ''' SELECT a.nom_facturation, a.rue AS rue_facturation, a.ville AS ville_facturation, a.code_postal AS code_postal_facturation,
                       a2.nom_facturation as nom_livraison, a2.rue AS rue_livraison, a2.ville AS ville_livraison, a2.code_postal AS code_postal_livraison
                FROM commande
                LEFT JOIN adresse a on a.id_adresse = commande.adresse_facturation
                LEFT JOIN adresse a2 on a2.id_adresse = commande.adresse_livraison
                WHERE id_commande = %s;   '''
        mycursor.execute(sql, (id_commande),)
        commande_adresses = mycursor.fetchone()
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , boissons_commande=boissons_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get', 'post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande set etat_id = 3 where id_commande = %s'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
