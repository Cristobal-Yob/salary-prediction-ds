from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return 'Hello world'

@app.route("/insert/<data>")
def get_data(data):
    data_dict = {}
    query = request.args.get('query')
    if query:
        data_dict['query'] = query
    return jsonify(data_dict)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        required_keys = ['python', 'excel', 'sql', 'aws', 'grouped_rating', 'group_title', 'group_sector']
        if not all(key in data for key in required_keys):
            return jsonify({'error': 'Missing required keys in request data'}), 400

        answers = [
            1 if data['python'] == 'yes' else 0,
            1 if data['excel'] == 'yes' else 0,
            1 if data['sql'] == 'yes' else 0,
            1 if data['aws'] == 'yes' else 0,
            {
                'up_to_2': 1,
                '2_to_2.5': 2,
                '2.5_to_3': 3,
                '3_to_3.5': 4,
                '3.5_to_4': 5,
                '4_to_4.5': 6,
                '4.5_to_5': 7
            }[data['grouped_rating']],
            {
                'rest': 1,
                'data_engineer': 2,
                'data_scientist': 3,
                'ml_engineer': 4
            }[data['group_title']],
            {
                'biotech_pharma': 1,
                'business_services': 2,
                'health_care': 3,
                'it': 4,
                'insurance': 5,
                'rest': 6
            }[data['group_sector']]
        ]

        input_variables = np.zeros(21)
        input_variables[0] = answers[0]
        input_variables[1] = answers[1]
        input_variables[2] = answers[2]
        input_variables[3] = answers[3]
        input_variables[4 + (answers[4] - 2)] = 1
        input_variables[11 + (answers[5] - 1)] = 1
        input_variables[15 + (answers[6] - 1)] = 1

        try:
            model_2 = joblib.load('modelo_001_salary_pred.pkl')
        except FileNotFoundError:
            return jsonify({'error': 'Model file not found'}), 500

        columns = ['Python', 'excel', 'sql', 'aws', 'Grouped_Rating_2.0', 
           'Grouped_Rating_2.5', 'Grouped_Rating_3.0', 'Grouped_Rating_3.5', 
           'Grouped_Rating_4.0', 'Grouped_Rating_4.5', 'Grouped_Rating_5.0', 
           'group_title_Rest', 'group_title_data engineer', 
           'group_title_data scientist', 'group_title_machine learning engineer', 
           'group_sector_Biotech & Pharmaceuticals', 'group_sector_Business Services', 
           'group_sector_Health Care', 'group_sector_Information Technology', 
           'group_sector_Insurance', 'group_sector_Rest']
        respuesta = input_variables.reshape(1, -1)
        X_new_df = pd.DataFrame(respuesta, columns=columns) 
        
        predicciones = model_2.predict(X_new_df)

        return jsonify({'prediction': predicciones[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
"""