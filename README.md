<div align="center">
  <h1>Used Car Price Prediction with Machine Learning</h1>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Machine%20Learning-Regression-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Model-CatBoost%20Regressor-lightblue?style=flat-square"/>
  <img src="https://img.shields.io/badge/App-Flask-success?style=flat-square"/>
  <img src="https://img.shields.io/badge/Pipeline-End--to--End%20ML-orange?style=flat-square"/>
</p>

---

## Project Overview

This project is an end-to-end machine learning application for estimating used car prices. It combines data cleaning, exploratory analysis, preprocessing, regression modeling, and a simple Flask web interface that allows users to enter vehicle details and receive a real-time price prediction.

The goal is to support better pricing decisions for second-hand cars by using historical listing data and key vehicle attributes.

---

## Business Problem

Used car prices can vary significantly depending on brand, model, year, mileage, fuel type, transmission, engine size, and ownership history. Buyers and sellers often need a reliable estimate to avoid overpaying, underpricing, or making decisions based only on intuition.

This project addresses that problem by building a predictive model that estimates a fair market price from structured car information.

---

## Objective

The objective of this project is to build a regression-based machine learning system that can:

- Predict used car prices from vehicle attributes
- Compare and evaluate different modeling approaches
- Preserve preprocessing consistency between training and inference
- Serve predictions through an interactive web application

---

## Data & Inputs

The model uses structured car listing data with features such as:

- Brand and model
- Manufacturing year
- Engine size
- Fuel type
- Transmission type
- Mileage
- Number of doors
- Previous owner count
- Listed price as the prediction target

The raw dataset is stored in `data/raw_data.xlsx`.

---

## Technical Approach

1. Data Cleaning  
   Cleaned the raw car listing data, handled data quality issues, and prepared the dataset for analysis.

2. Exploratory Data Analysis  
   Explored relationships between price and vehicle characteristics to understand important pricing patterns.

3. Feature Engineering & Preprocessing  
   Encoded categorical variables, prepared numerical features, and saved preprocessing objects for reuse during inference.

4. Model Training  
   Tested regression models and selected a tree-based ensemble approach, with the final model saved for deployment.

5. Web Deployment  
   Built a Flask application that loads the trained model and encoders, collects user inputs, preprocesses them, and returns a predicted car price.

---

## Repository Structure

```text
.
├── app.py                         # Flask application for prediction
├── data/
│   └── raw_data.xlsx              # Raw car listing dataset
├── models/
│   ├── Brand_Encoder.pkl          # Saved brand encoder
│   ├── Model_Encoder.pkl          # Saved model encoder
│   ├── OneHot_Encoder.pkl         # Saved one-hot encoder
│   └── model.pkl                  # Trained regression model
├── src/
│   ├── cleaning.ipynb             # Data cleaning workflow
│   ├── eda.ipynb                  # Exploratory data analysis
│   ├── preprocessing.ipynb        # Feature engineering and preprocessing
│   ├── splitting.ipynb            # Train/test split workflow
│   └── modelling/
│       └── algorithm_testing.ipynb
├── templates/
│   └── index.html                 # Web application interface
├── requirements.txt               # Python dependencies
├── runtime.txt                    # Runtime configuration
└── README.md
```

---

## How to Run the Project

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask application:

```bash
python app.py
```

Open the app in your browser:

```text
http://127.0.0.1:5001
```

---

## Application Inputs

The web app asks the user to provide:

- Car brand and model
- Fuel type
- Transmission type
- Manufacturing year
- Engine size
- Mileage
- Number of doors
- Number of previous owners

After submitting the form, the application returns an estimated used car price.

---

## Key Skills Demonstrated

- Supervised machine learning for regression
- Data cleaning and exploratory data analysis
- Feature engineering for categorical and numerical data
- Model evaluation and algorithm comparison
- Saving and reusing trained models and encoders
- Building an end-to-end inference pipeline
- Deploying a machine learning model with Flask

---

## Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- CatBoost
- XGBoost
- Matplotlib, Seaborn
- Flask
- HTML/CSS

---

## Future Improvements

- Add model performance metrics to the README
- Add API-based prediction support with JSON input
- Improve handling for unseen brands or models
- Add automated tests for preprocessing and prediction logic
- Deploy the application to a cloud platform
