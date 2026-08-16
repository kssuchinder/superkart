import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load the serialized model
model = joblib.load('superkart_model.joblib')

@app.route('/')
def home():
    return 'SuperKart Sales Prediction API is running!'

# Define prediction endpoint for single inference
@app.route('/v1/predict', methods=['POST'])
def predict_single():
    try:
        json_payload = request.get_json()
        input_df = pd.DataFrame([json_payload])

        # Make prediction
        prediction = model.predict(input_df)[0]

        return jsonify({'prediction': prediction.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Define prediction endpoint for batch inference
@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and file.filename.endswith('.csv'):
            input_df = pd.read_csv(file)
            predictions = model.predict(input_df)

            return jsonify({'predictions': predictions.tolist()})
        else:
            return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# To run the app (only when executing this file directly)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=7860)
