from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

import os                                 # à ajouter
from dotenv import load_dotenv            # à ajouter
#load_dotenv()
project_folder = os.path.expanduser('~/SAE-3-4-5')  # adjust as appropriate (avec le dossier où se trouve le fichier .env et app.py)
load_dotenv(os.path.join(project_folder, '.env'))
def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host=os.environ.get("HOST"),                # à modifier
            user=os.environ.get("LOGIN"),               # à modifier
            password=os.environ.get("PASSWORD"),        # à modifier
            database=os.environ.get("DATABASE"),        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db