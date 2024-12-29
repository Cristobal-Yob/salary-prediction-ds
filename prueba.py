from flask import Flask, render_template, request
import joblib
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
with open('modelo_001_salary_pred.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/project1')
def project1():
    return render_template('project1.html')

@app.route('/project2')
def project2():
    return render_template('project2.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    # Initialize the input variables with zeros

    #answers = [1, 1, 1, 1, 5, 3, 4]
    answers = [
        1 if data['python'] == 'yes' else 0,
        1 if data['excel'] == 'yes' else 0,
        1 if data['sql'] == 'yes' else 0,
        1 if data['aws'] == 'yes' else 0,
        {
            'up_to_2': 2,
            '2_to_2.5': 2.5,
            '2.5_to_3': 3,
            '3_to_3.5': 3.5,
            '3.5_to_4': 4,
            '4_to_4.5': 4.5,
            '4.5_to_5': 5
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
    input_variables[1] = answers[1]  # excel
    input_variables[2] = answers[2]  # sql
    input_variables[3] = answers[3]  # aws

    # Grouped_Rating
    input_variables[4 + (answers[4] - 2)] = 1  # Grouped_Rating_2.0 to Grouped_Rating_5.0

    # group_title
    if answers[5] == 1:
        input_variables[11] = 1  # group_title_Rest
    elif answers[5] == 2:
        input_variables[12] = 1  # group_title_data engineer
    elif answers[5] == 3:
        input_variables[13] = 1  # group_title_data scientist
    elif answers[5] == 4:
        input_variables[14] = 1  # group_title_machine learning engineer

    # group_sector
    if answers[6] == 1:
        input_variables[15] = 1  # group_sector_Biotech & Pharmaceuticals
    elif answers[6] == 2:
        input_variables[16] = 1  # group_sector_Business Services
    elif answers[6] == 3:
        input_variables[17] = 1  # group_sector_Health Care
    elif answers[6] == 4:
        input_variables[18] = 1  # group_sector_Information Technology
    elif answers[6] == 5:
        input_variables[19] = 1  # group_sector_Insurance
    elif answers[6] == 6:
        input_variables[20] = 1  # group_sector_Rest

    # Convierte a formato adecuado para el modelo
    respuesta = input_variables.reshape(1, -1)

    # Carga el modelo entrenado
    import joblib
    model_2 = joblib.load('modelo_001_salary_pred.pkl')

    # Predice el salario usando el modelo cargado
    predicciones = model_2.predict(respuesta)

    return render_template('result.html', prediction=predicciones[0])

if __name__ == '__main__':
    app.run(debug=True)