from flask import Flask, request, jsonify, render_template
from sklearn.linear_model import LinearRegression
import pickle

lr_model = pickle.load(open('../model/model.sav', 'rb'))
columns = ['MSZoning', 'LotArea', 'Street', 'Utilities', 'OverallCond', 'YearBuilt', 'FullBath', 'BedroomAbvGr', 'KitchenAbvGr', 'GarageCars', 'MSSubClass']

app = Flask('housing_prices')

@app.route('/v1')
def healthCheck():
    return "Housing Prices API V1.0.0."

@app.route('/v1/home')
def home():
    return render_template('index.html')

@app.route('/v1/quotation', methods=['POST'])
def quotation():
    data = request.get_json()
    data_input = [data[col] for col in columns]
    price = lr_model.predict([data_input])
    return jsonify(price=price[0])

app.run(debug=True)