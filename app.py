import os
import pickle
from flask import Flask, request, jsonify, url_for, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from catboost import CatBoostRegressor


# create an app instance
app = Flask(__name__)

MODEL_OPTIONS = {
    "Audi": ["A3", "A4", "Q5"],
    "BMW": ["3 Series", "5 Series", "X5"],
    "Chevrolet": ["Equinox", "Impala", "Malibu"],
    "Ford": ["Explorer", "Fiesta", "Focus"],
    "Honda": ["Accord", "CR-V", "Civic"],
    "Hyundai": ["Elantra", "Sonata", "Tucson"],
    "Kia": ["Optima", "Rio", "Sportage"],
    "Mercedes": ["C-Class", "E-Class", "GLA"],
    "Toyota": ["Camry", "Corolla", "RAV4"],
    "Volkswagen": ["Golf", "Passat", "Tiguan"],
}

FUELS = ["Diesel", "Electric", "Hybrid", "Petrol"]
TRANSMISSIONS = ["Automatic", "Manual", "Semi-Automatic"]
YEARS = list(range(2000, 2024))
DOORS = [1, 2, 3, 4, 5]
OWNER_COUNTS = [1, 2, 3, 4, 5]


def model_path(filename):
    return os.path.join(app.root_path, "models", filename)


with open(model_path('model.pkl'), 'rb') as f:
    price_model = pickle.load(f)
with open(model_path('Brand_Encoder.pkl'), 'rb') as f:
    Brand_Encoder = pickle.load(f)
with open(model_path('Model_Encoder.pkl'), 'rb') as f:
    Model_Encoder = pickle.load(f)
with open(model_path('OneHot_Encoder.pkl'), 'rb') as f:
    OneHot_Encoder = pickle.load(f)


def encoded_mean(encoder):
    values = pd.Series(encoder.to_numpy(), dtype="float64")
    return values.mean()


def parse_prediction_payload(payload):
    return {
        "brand": payload["Brand"],
        "car_model": payload["Model"],
        "fuel": payload["Fuel"],
        "transmission": payload["Transmission"],
        "year": int(payload["Year"]),
        "engine_size": float(payload["EngineSize"]),
        "mileage": int(payload["Mileage"]),
        "doors": int(payload["Doors"]),
        "owner_counts": int(payload["OwnerCount"]),
    }


def predict_price(payload):
    input_df = pd.DataFrame({
        'Brand': [payload["brand"]],
        'Model': [payload["car_model"]],
        'Year': [payload["year"]],
        'EngineSize': [payload["engine_size"]],
        'Fuel': [payload["fuel"]],
        'Transmission': [payload["transmission"]],
        'Mileage': [payload["mileage"]],
        'Doors': [payload["doors"]],
        'OwnerCount': [payload["owner_counts"]]
    })

    # Encode Brand and Model with the same target encoders used during training.
    input_df['Encoded_Brand'] = input_df['Brand'].map(Brand_Encoder)
    input_df['Encoded_Model'] = input_df['Model'].map(Model_Encoder)
    input_df['Encoded_Brand'] = input_df['Encoded_Brand'].fillna(encoded_mean(Brand_Encoder))
    input_df['Encoded_Model'] = input_df['Encoded_Model'].fillna(encoded_mean(Model_Encoder))
    input_df.drop(['Brand', 'Model'], axis=1, inplace=True)

    categorical_cols = ['Fuel', 'Transmission']
    encoded_array = OneHot_Encoder.transform(input_df[categorical_cols])
    if hasattr(encoded_array, "toarray"):
        encoded_array = encoded_array.toarray()
    encoded_df = pd.DataFrame(
        encoded_array,
        columns=OneHot_Encoder.get_feature_names_out(categorical_cols)
    )

    input_df_encoded = input_df.drop(columns=categorical_cols).reset_index(drop=True)
    input_data = pd.concat([input_df_encoded, encoded_df], axis=1)
    prediction = price_model.predict(input_data)
    return round(float(prediction[0]), 2)


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/api/options", methods=['GET'])
def api_options():
    return jsonify({
        "brands": list(MODEL_OPTIONS.keys()),
        "models": MODEL_OPTIONS,
        "fuels": FUELS,
        "transmissions": TRANSMISSIONS,
        "years": YEARS,
        "doors": DOORS,
        "ownerCounts": OWNER_COUNTS
    })


@app.route("/api/predict", methods=['POST'])
def api_predict():
    try:
        payload = parse_prediction_payload(request.get_json(force=True))
        output = predict_price(payload)
        if output < 0:
            return jsonify({"prediction": output, "message": "Car cannot be sold."}), 422
        return jsonify({
            "prediction": output,
            "currency": "USD",
            "message": "The car is worth ${:,.2f}".format(output)
        })
    except KeyError as error:
        return jsonify({"error": "Missing field: {}".format(error.args[0])}), 400
    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        payload = parse_prediction_payload(request.form)
        output = predict_price(payload)
        
        if output < 0:
            return render_template('index.html', prediction_texts="car cannot be sold!")
        else:
            return render_template('index.html', prediction_text="the car worth: $ {}".format(output))
    else:
        return render_template('index.html')
        
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
