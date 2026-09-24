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

# Group car models by company for dynamic frontend filtering
company_models = car.groupby('company')['name'].apply(lambda x: sorted(x.unique().tolist())).to_dict()

def format_inr(number):
    s = str(int(round(number)))
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rem = s[:-3]
    parts = []
    while len(rem) > 2:
        parts.append(rem[-2:])
        rem = rem[:-2]
    parts.append(rem)
    return ','.join(reversed(parts)) + ',' + last3

@app.route('/', methods=['GET', 'POST'])
def index():
    companies = sorted(car['company'].fillna('').astype(str).dropna().unique())
    car_models = sorted(car['name'].fillna('').astype(str).dropna().unique())
    years = sorted(car['year'].dropna().astype(int).unique(), reverse=True)
    fuel_types = sorted(car['fuel_type'].fillna('').astype(str).dropna().unique())

    prediction = None
    form_data = {}

    if request.method == 'POST':
        try:
            company = request.form.get('company', '').strip()
            car_model = request.form.get('car_model', '').strip()
            year = int(request.form.get('year', 0))
            kms_driven = int(request.form.get('kms_driven', 0))
            fuel_type = request.form.get('fuel_type', '').strip()

            form_data = {
                'company': company,
                'car_model': car_model,
                'year': year,
                'kms_driven': kms_driven,
                'fuel_type': fuel_type
            }

            payload = {
                'Name': car_model,
                'company': company,
                'year': year,
                'kms_driven': kms_driven,
                'fuel_type': fuel_type,
            }
            df = pd.DataFrame([payload])
            pred_val = model.predict(df[['Name', 'company', 'year', 'kms_driven', 'fuel_type']])[0]

            if pred_val > 0:
                prediction = format_inr(pred_val)
            else:
                prediction = "0 (Valuation unavailable for entered parameters)"
        except Exception as exc:
            prediction = f"Error: {exc}"

    return render_template(
        'index.html',
        companies=companies,
        car_models=car_models,
        years=years,
        fuel_types=fuel_types,
        company_models=company_models,
        prediction=prediction,
        form_data=form_data,
    )

if __name__ == '__main__':
    app.run(debug=True)
