import pickle
from flask import Flask, request, jsonify, url_for, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from catboost import CatBoostRegressor


# create an app instance
app = Flask(__name__)
with open('./models/Model.pkl', 'rb') as f:
    price_model = pickle.load(f)
with open('./models/Brand_Encoder.pkl', 'rb') as f:
    Brand_Encoder = pickle.load(f)
with open('./models/Model_Encoder.pkl', 'rb') as f:
    Model_Encoder = pickle.load(f)
with open('./models/OneHot_Encoder.pkl', 'rb') as f:
    OneHot_Encoder = pickle.load(f)

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        # extract form data
        brand = request.form['Brand']
        car_model = request.form['Model']
        fuel = request.form['Fuel']
        transmission = request.form['Transmission']
        year = int(request.form['Year'])
        engine_size = float(request.form['EngineSize'])
        mileage = int(request.form['Mileage'])
        doors = int(request.form['Doors'])
        owner_counts = int(request.form['OwnerCount'])

        # create dataframe for the input data
        input_df = pd.DataFrame({
            'Brand': [brand],
            'Model': [car_model],
            'Year': [year],
            'EngineSize': [engine_size],
            'Fuel': [fuel],
            'Transmission': [transmission],
            'Mileage': [mileage],
            'Doors': [doors],
            'OwnerCount': [owner_counts]
        })
    
        # encode Brand and Model using mean target encoding
        input_df['Encoded_Brand'] = input_df['Brand'].map(Brand_Encoder)
        input_df['Encoded_Model'] = input_df['Model'].map(Model_Encoder)
        input_df['Encoded_Brand'].fillna(input_df['Encoded_Brand'].mean(), inplace=True)
        input_df['Encoded_Model'].fillna(input_df['Encoded_Model'].mean(), inplace=True)
        input_df.drop(['Brand', 'Model'], axis=1, inplace=True)
        
        # one-hot encode Fuel and Transmission
        categorical_cols = ['Fuel', 'Transmission']
        encoded_array = OneHot_Encoder.transform(input_df[categorical_cols])
        encoded_df = pd.DataFrame(encoded_array, columns=OneHot_Encoder.get_feature_names_out(categorical_cols))
        
        # merge encoded columns with input data
        input_df_encoded = input_df.drop(columns=categorical_cols).reset_index(drop=True)
        input_data = pd.concat([input_df_encoded, encoded_df], axis=1)
        
        # make prediction
        prediction = price_model.predict(input_data)
        output = round(prediction[0], 2)
        
        if output < 0:
            return render_template('index.html', prediction_texts="car cannot be sold!")
        else:
            return render_template('index.html', prediction_text="the car worth: $ {}".format(output))
    else:
        return render_template('index.html')
        
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
