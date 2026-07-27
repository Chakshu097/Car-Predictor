import os
import pickle
import pandas as pd
from flask import Flask, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'Cleaned Car.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'LinearRegressionModel.pkl')

app = Flask(__name__, template_folder='templates', static_folder='static')

car = pd.read_csv(CSV_PATH)
car.columns = [str(col).strip().lower().replace(' ', '_') for col in car.columns]
car = car.loc[:, ~car.columns.duplicated()]

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    companies = sorted(car['company'].fillna('').astype(str).dropna().unique())
    car_models = sorted(car['name'].fillna('').astype(str).dropna().unique())
    years = sorted(car['year'].dropna().astype(int).unique(), reverse=True)
    fuel = sorted(car['fuel_type'].fillna('').astype(str).dropna().unique())

    prediction = None
    if request.method == 'POST':
        try:
            payload = {
                'Name': request.form.get('car_model', '').strip(),
                'company': request.form.get('company', '').strip(),
                'year': int(request.form.get('year', 0)),
                'kms_driven': int(request.form.get('kms_driven', 0)),
                'fuel_type': request.form.get('fuel_type', '').strip(),
            }
            df = pd.DataFrame([payload])
            prediction = model.predict(df[['Name', 'company', 'year', 'kms_driven', 'fuel_type']])[0]
            prediction = round(float(prediction), 2)
        except Exception as exc:
            prediction = f'Error: {exc}'

    return render_template(
        'index.html',
        companies=companies,
        car_models=car_models,
        years=years,
        fuel_types=fuel,
        prediction=prediction,
    )

if __name__ == '__main__':
    app.run(debug=True)
