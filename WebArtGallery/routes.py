from flask import render_template, redirect, request
from sqlalchemy import create_engine
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

@app.route("/")
def index():
   return "Hello World"