from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    size = data["size"]
    bedrooms = data["bedrooms"]

    prediction = model.predict([
        [size, bedrooms]
    ])

    return jsonify({
        "prediction": float(prediction[0])
    })


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)