import json
from flask import Flask, request, jsonify
import sqlite3
import os
import aspose.cells
from aspose.cells import Workbook
import pandas as pd

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaah"

"""@app.route('/app/db', methods=['GET'])
def crear_db():

    df = pd.read_csv("data/Advertising.csv", index_col=False)
    df.drop("Unnamed: 0", axis = 1)
    df["newpaper"] = df["newpaper"].str.replace("s","")
    df['newpaper'] = df['newpaper'].astype(float)
    conn = sqlite3.connect("data/Advert.db")
    df.to_sql("Advertising", conn, index=False, if_exists="replace")
    conn.close()
    return 'Completado, puedes salir de la pestaña.'"""

@app.route('/v2/predict', methods=['GET'])
def prediccion():
    connection = sqlite3.connect("data/Advert.db")
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM Advertising;")
    rows = crsr.fetchall()
    connection.close()
    return rows

app.run()

