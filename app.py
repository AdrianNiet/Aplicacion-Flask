import json
from flask import Flask, request, jsonify
import sqlite3
import os
import aspose.cells
from aspose.cells import Workbook
import pandas as pd
import joblib
import pickle
from sklearn.model_selection import train_test_split

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

@app.route('/v2/test', methods=['GET'])
def test():
    connection = sqlite3.connect("data/Advert.db")
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM Advertising;")
    rows = crsr.fetchall()
    connection.close()
    return rows

@app.route('/v2/pred', methods=['GET'])
def prediction():
    modelo = joblib.load("data/advertising_model.pkl")
    conexion = sqlite3.connect("data/Advert.db")
    consulta_sql = "SELECT * FROM Advertising;"
    df = pd.read_sql_query(consulta_sql, conexion)
    test = df.drop(["sales"],axis=1)
    predictions = modelo.predict(test)
    predictions = (list(predictions))

    return predictions

@app.route('/v2/ingest_data', methods=['GET'])

def ingest():
    connection = sqlite3.connect("data/Advert.db")
    crsr = connection.cursor()
    datos = {}
    datos['TV'] = float(request.args['TV'])
    datos['radio'] = float(request.args['radio'])
    datos['newspaper'] = float(request.args['newspaper'])
    datos['sales'] = float(request.args['sales'])
    nuevos_valores = (
        datos.get('TV'),
        datos.get('radio'),
        datos.get('newspaper'),
        datos.get('sales')
    )
    crsr.execute("INSERT INTO Advertising (TV, radio, newspaper, sales) VALUES (?, ?, ?, ?);", nuevos_valores)
    connection.commit()
    connection.close()
    return datos

@app.route('/v2/retrain', methods=['GET'])

def reentrenar():
    modelo = joblib.load("data/advertising_model.pkl")
    conexion = sqlite3.connect("data/Advert.db")
    consulta_sql = "SELECT * FROM Advertising;"
    df = pd.read_sql_query(consulta_sql, conexion)
    modelo.fit(df.drop(["sales"],axis=1), df["sales"])
    with open('advertising_model.pkl', 'wb') as archivo:
        pickle.dump(modelo, archivo)
    return "Modelo Re-entrenado"
app.run()

