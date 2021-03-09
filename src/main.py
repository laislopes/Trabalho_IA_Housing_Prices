from flask import Flask, request, jsonify
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("../dataset/train.csv")
columns = ['SalePrice','MSZoning', 'LotArea', 'Street', 'Utilities', 'OverallCond', 'YearBuilt', 'FullBath', 'BedroomAbvGr', 'KitchenAbvGr', 'GarageCars', 'MSSubClass']
df = df[columns]

le = LabelEncoder()

df['MSZoning'] = le.fit_transform(df['MSZoning'])
df['Street'] = le.fit_transform(df['Street'])
df['Utilities'] = le.fit_transform(df['Utilities'])

X = df.drop(['SalePrice'], axis = 1)
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state = 4)

lr_model = LinearRegression() 
lr_model.fit(X_train, y_train)
columns.remove('SalePrice')

app = Flask('housing_prices')

@app.route('/v1')
def healthCheck():
    return "Housing Prices API V1.0.0."

@app.route('/v1/quotation', methods=['POST'])
def quotation():
    data = request.get_json()
    data_input = [data[col] for col in columns]
    price = lr_model.predict([data_input])
    return jsonify(price=price[0])

app.run(debug=True)