from flask import render_template, redirect, request
from sqlalchemy import create_engine, text
import pandas as pd
from WebArtGallery import app
import os

def connect():
    user = os.getenv('EXHIBIT_SQL_USER')
    password = os.getenv('EXHIBIT_SQL_PASSWORD')
    database = os.getenv('EXHIBIT_SQL_DATABASE')
    server = os.getenv('EXHIBIT_SQL_SERVER')
    url = f'mysql+mysqlconnector://{user}:{password}@{server}/{database}'
    engine = create_engine(url)
    return engine

@app.route("/", methods = ['GET','POST'])
def index():
    engine= connect()
    if request.method == 'POST':
        query_data = request.form
        # first queery
        if query_data['onechoice'] == 'queery 1':
            print(query_data['mediumList'])
            with engine.connect() as con:
                rs = con.execute(text(f"""SELECT DISTINCT   A.artistID, A.artistName
                           FROM     Artist AS A, Artwork AS R
                           WHERE    A.artistID=R.artistID AND R.medium='{query_data['mediumList']}'"""))
                for row in rs:
                    print(row)
            medium = request.form.get('mediumList')
        # secind queery goes here
        print(request.values)
        # elif query == 'queery 2':
        #     print('blahhh......')
        # print(query, medium)
    return render_template("helloworld.html")

@app.route("/sayhello/<name>")
def sayhello(name):
    return render_template("helloworld.html", name = name)