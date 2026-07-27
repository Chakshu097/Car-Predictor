from pathlib import Path

app_code = '''import os
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
'''

html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Car Price Predictor</title>
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <div class="card shadow">
        <div class="card-header bg-dark text-white text-center">
          <h2>Car Price Predictor</h2>
        </div>
        <div class="card-body">
          <form method="post">
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>Company</label>
                <select class="form-control" name="company" required>
                  {% for item in companies %}
                  <option value="{{ item }}">{{ item }}</option>
                  {% endfor %}
                </select>
              </div>
              <div class="form-group col-md-6">
                <label>Car Model</label>
                <select class="form-control" name="car_model" required>
                  {% for item in car_models %}
                  <option value="{{ item }}">{{ item }}</option>
                  {% endfor %}
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-4">
                <label>Year</label>
                <select class="form-control" name="year" required>
                  {% for item in years %}
                  <option value="{{ item }}">{{ item }}</option>
                  {% endfor %}
                </select>
              </div>
              <div class="form-group col-md-4">
                <label>Kilometers Driven</label>
                <input type="number" class="form-control" name="kms_driven" required min="0">
              </div>
              <div class="form-group col-md-4">
                <label>Fuel Type</label>
                <select class="form-control" name="fuel_type" required>
                  {% for item in fuel_types %}
                  <option value="{{ item }}">{{ item }}</option>
                  {% endfor %}
                </select>
              </div>
            </div>
            <button type="submit" class="btn btn-primary">Predict Price</button>
          </form>

          {% if prediction is not none %}
          <div class="alert alert-info mt-4">
            <strong>Predicted Price:</strong> ₹{{ prediction }}
          </div>
          {% endif %}
        </div>
      </div>
    </div>
  </body>
</html>
'''

css = '''body {
    background: #f4f7fb;
    font-family: Arial, sans-serif;
}

.card {
    border-radius: 12px;
}

.btn-primary {
    background-color: #0d6efd;
    border: none;
}

.alert-info {
    background-color: #e9f5ff;
    color: #0c5460;
}
'''

Path('d:/car predictor/application.py').write_text(app_code, encoding='utf-8')
Path('d:/car predictor/templates').mkdir(parents=True, exist_ok=True)
Path('d:/car predictor/templates/index.html').write_text(html, encoding='utf-8')
Path('d:/car predictor/static').mkdir(parents=True, exist_ok=True)
Path('d:/car predictor/static/style.css').write_text(css, encoding='utf-8')
print('wrote application.py, templates/index.html, static/style.css')
