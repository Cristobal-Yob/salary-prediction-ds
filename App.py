from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

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
        # Carga los datos del cuerpo de la solicitud
        data = request.json

        # Validación de claves requeridas
        required_keys = ['python', 'excel', 'sql', 'aws', 'grouped_rating', 'group_title', 'group_sector']
        if not all(key in data for key in required_keys):
            return jsonify({'error': 'Missing required keys in request data'}), 400

        # Procesa las respuestas del formulario
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

        # Inicializa las variables de entrada con ceros
        input_variables = np.zeros(21)

        # Mapea las respuestas a las variables correspondientes
        input_variables[0] = answers[0]  # Python
        input_variables[1] = answers[1]  # Excel
        input_variables[2] = answers[2]  # SQL
        input_variables[3] = answers[3]  # AWS
        input_variables[4 + (answers[4] - 2)] = 1  # Grouped_Rating
        input_variables[11 + (answers[5] - 1)] = 1  # Group_Title
        input_variables[15 + (answers[6] - 1)] = 1  # Group_Sector

        # Carga el modelo entrenado
        try:
            model_2 = joblib.load('modelo_001_salary_pred.pkl')
        except FileNotFoundError:
            return jsonify({'error': 'Model file not found'}), 500

        # Predice el salario
        respuesta = input_variables.reshape(1, -1)
        predicciones = model_2.predict(respuesta)

        return jsonify({'prediction': predicciones[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
