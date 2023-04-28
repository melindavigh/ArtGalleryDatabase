from flask import Flask, render_template
import json
app = Flask(__name__)


with open("config.json") as config_file:
    config = json.load(config_file)


    from WebArtGallery import routes
