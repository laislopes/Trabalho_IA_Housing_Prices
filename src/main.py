from flask import Flask, request, jsonify, render_template
from sklearn.linear_model import LinearRegression
import pickle
import locale


lr_model = pickle.load(open('../model/model.sav', 'rb'))
columns = ['LotArea', 'Street', 'Utilities', 'BedroomAbvGr']

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
    locale.setlocale(locale.LC_ALL, 'en_US')
    price = locale.currency(price, grouping=True)
    return render_template('price.html', price=price)

@app.route('/v1/about')
def about():
    return render_template('about.html')

app.run(debug=True)
