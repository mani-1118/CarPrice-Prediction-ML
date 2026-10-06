from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Load trained ML model
model = joblib.load("models/car_price_model.pkl")

# OpenAI client
client = OpenAI()


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    car_data = pd.DataFrame([{
        "Car_Name": data["Car_Name"],
        "Year": int(data["Year"]),
        "Present_Price": float(data["Present_Price"]),
        "Kms_Driven": int(data["Kms_Driven"]),
        "Fuel_Type": data["Fuel_Type"],
        "Seller_Type": data["Seller_Type"],
        "Transmission": data["Transmission"],
        "Owner": int(data["Owner"])
    }])

    prediction = model.predict(car_data)[0]

    return jsonify({
        "predicted_price": round(float(prediction), 2)
    })


@app.route("/ai-advice", methods=["POST"])
def ai_advice():

    data = request.get_json()

    car_name = data["Car_Name"]
    year = data["Year"]
    present_price = data["Present_Price"]
    kms_driven = data["Kms_Driven"]
    fuel_type = data["Fuel_Type"]
    seller_type = data["Seller_Type"]
    transmission = data["Transmission"]
    owner = data["Owner"]
    predicted_price = data["predicted_price"]

    prompt = f"""
You are an AI car advisor inside a used-car price prediction application.

Give the user a short, practical explanation of their estimated car value.

Vehicle details:
- Car model: {car_name}
- Manufacturing year: {year}
- Current/original price: ₹{present_price} Lakhs
- Kilometers driven: {kms_driven} km
- Fuel type: {fuel_type}
- Seller type: {seller_type}
- Transmission: {transmission}
- Previous owners: {owner}
- ML estimated selling price: ₹{predicted_price} Lakhs

Your response must:
1. Explain briefly why these vehicle factors can affect resale value.
2. Give 2 or 3 practical selling tips.
3. Be easy for a normal car owner to understand.
4. Do not claim that the estimate is an exact market price.
5. Keep the response under 120 words.
6. Do not mention model accuracy, R², MAE, RMSE, or technical ML metrics.

Return only the advice text.
"""

    try:

        response = client.responses.create(
            model="gpt-6-luna",
            input=prompt
        )

        advice = response.output_text

        return jsonify({
            "advice": advice
        })

    except Exception as error:

        print("GenAI error:", error)

        return jsonify({
            "error": "Unable to generate AI advice."
        }), 500


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Used Car Price Prediction API is running"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
