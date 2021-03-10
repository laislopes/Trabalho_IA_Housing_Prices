from flask import Flask, request, jsonify, render_template
from sklearn.linear_model import LinearRegression
import pickle

lr_model = pickle.load(open('../model/model.sav', 'rb'))
columns = ['MSZoning', 'LotArea', 'Street', 'Utilities', 'OverallCond', 'YearBuilt', 'FullBath', 'BedroomAbvGr', 'KitchenAbvGr', 'GarageCars']

app = Flask('housing_prices')

@app.route('/v1')
def healthCheck():
    return "Housing Prices API V1.0.0."

@app.route('/v1/home')
def home():
    return render_template('index.html')

@app.route('/v1/quotation', methods=['POST'])
def quotation():
    
    data_input = [int(request.form[col]) for col in columns]
    print(data_input)
    price = lr_model.predict([data_input])[0]
    return render_template('price.html', price=price)

app.run(debug=True)