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

@app.route('/v2/test', methods=['GET'])
def test():
    connection = sqlite3.connect("data/Advert.db")
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM Advertising;")
    rows = crsr.fetchall()
    connection.close()
    return rows

@app.route('/v2/predict', methods=['GET'])
def prediction():
    modelo = joblib.load("data/advertising_model.pkl")
    conexion = sqlite3.connect("data/Advert.db")
    consulta_sql = "SELECT * FROM Advertising;"
    df = pd.read_sql_query(consulta_sql, conexion)
    test = df.drop(["sales"],axis=1)
    predictions = modelo.predict(test)
    predictions = (list(predictions))

    return predictions

@app.route('/v2/ingest', methods=['POST'])

def ingest():
    connection = sqlite3.connect("data/Advert.db")
    crsr = connection.cursor()
    datos = request.json

    tv = float(datos['TV'])
    radio = float(datos['radio'])
    newspaper = float(datos['newspaper'])
    sales = float(datos['sales'])
    
    crsr.execute("INSERT INTO Advertising (TV, radio, newspaper, sales) VALUES (?, ?, ?, ?);", datos)
    connection.commit()
    connection.close()
    return "Datos ingresados correctamente"

@app.route('/v2/retrain', methods=['POST'])

def reentrenar():
    modelo = joblib.load("data/advertising_model.pkl")
    conexion = sqlite3.connect("data/Advert.db")
    consulta_sql = "SELECT * FROM Advertising;"
    df = pd.read_sql_query(consulta_sql, conexion)
    modelo.fit(df.drop(["sales"],axis=1), df["sales"])
    with open('advertising_model.pkl', 'wb') as archivo:
        pickle.dump(modelo, archivo)
    return "Modelo reentrenado correctamente."


@app.route('/predict', methods=['GET'])
def prediction2():

    #cargamos el modelo
    model = pickle.load(open('data/advertising_model.pkl','rb'))
    data = request.get_json()
    #cojemos los valores de data, lo guardamos en una variable
    input_values = data['data'][0]
    tv, radio, newspaper = map(int, input_values)
    #predecimos con el valor que nos han dado.
    prediction = model.predict([[tv, radio, newspaper]])
    return jsonify({'prediction': round(prediction[0], 2)})



@app.route('/ingest', methods=['POST'])

def ingest2():
    connection = sqlite3.connect("data/Advert.db")
    crsr = connection.cursor()
    data = request.get_json()

    for row in data.get('data', []):
        tv, radio, newspaper, sales = row
        query = "INSERT INTO Advertising (tv, radio, newspaper, sales) VALUES (?, ?, ?, ?)"
        crsr.execute(query, (tv, radio, newspaper, sales))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Datos ingresados correctamente'})

@app.route('/retrain', methods=['POST'])
def reentrenar2():
    modelo = joblib.load("data/advertising_model.pkl")

    conexion = sqlite3.connect("data/Advert.db")

    consulta_sql = "SELECT * FROM Advertising;"

    df = pd.read_sql_query(consulta_sql, conexion)

    modelo.fit(df.drop(["sales"],axis=1), df["sales"])

    with open('advertising_model.pkl', 'wb') as archivo:
        pickle.dump(modelo, archivo)

    return jsonify({'message': 'Modelo reentrenado correctamente.'})

app.run()

