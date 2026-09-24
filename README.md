# Car Price Predictor

A machine learning web application that estimates the market value of used cars based on historical pricing data. Built with Flask and Scikit-learn, the application provides an interactive and user-friendly interface to evaluate car prices according to vehicle attributes.

## Live Demo

[Live Demo](https://car-predictor-denp.onrender.com)

## Overview

Car Price Predictor is designed to help buyers and sellers estimate reasonable resale prices for pre-owned vehicles. Users specify the car brand, model, purchase year, kilometers driven, and fuel type through an intuitive form, and the underlying trained Linear Regression model generates an estimated valuation in Indian Rupees (INR).

## Features

- **Dynamic Model Filtering**: Selecting a company dynamically updates the car model dropdown with corresponding vehicles from the dataset.
- **Used Car Valuation**: Predicts estimated resale value based on brand, model, registration year, distance traveled, and fuel type.
- **Indian Currency Formatting**: Outputs valuations formatted according to the Indian numbering system (e.g., ₹3,38,796) without unnecessary decimals.
- **Form State Retention**: Preserves user input selections after form submission for easy adjustments.
- **One-Click Form Reset**: Restores dropdowns and inputs back to default placeholder states and clears previous predictions.
- **Responsive Interface**: Clean and modern layout built with Bootstrap and custom CSS for desktop and mobile usability.

## Machine Learning Model

The valuation engine uses a **Linear Regression** algorithm trained on pre-processed historical car sales data:

- **Input Features**:
  - `Name`: Specific car model name (categorical)
  - `company`: Manufacturing brand (categorical)
  - `year`: Year of manufacture / registration (numerical)
  - `kms_driven`: Total distance driven in kilometers (numerical)
  - `fuel_type`: Fuel variant such as Petrol, Diesel, or LPG (categorical)
- **Preprocessing Pipeline**:
  - Categorical variables are encoded using `OneHotEncoder`.
  - Numerical features are scaled using `StandardScaler`.
  - Feature transformations and regression are encapsulated within a Scikit-learn `Pipeline` and `ColumnTransformer`.
- **Saved Model**: Serialized and loaded via `pickle` from `LinearRegressionModel.pkl`.

## Tech Stack

- Python
- Flask
- Pandas
- Scikit-learn
- HTML
- CSS
- JavaScript
- Bootstrap

## Project Structure

```
Car-Predictor/
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── .gitignore
├── application.py
├── Cleaned Car.csv
├── LinearRegressionModel.pkl
├── README.md
└── requirements.txt
```

## How to Run Locally

Clone the repository and set up a local virtual environment:

```bash
git clone https://github.com/Chakshu097/Car-Predictor.git
cd Car-Predictor
```

Create and activate a virtual environment:

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python application.py
```

Once started, open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

## Deployment

The application is structured to be deployed as a standard WSGI web service on cloud platforms such as Render, Railway, Heroku, or AWS.

For production deployment on Linux environments, the application can be served with **Gunicorn**:

```bash
gunicorn application:app
```

## Limitations

- Valuation results are statistical predictions derived from a finite historical dataset (`Cleaned Car.csv`) and should be treated as estimates rather than guaranteed market or dealer prices.
- Vehicle condition, accident history, insurance validity, regional demand, and cosmetic wear are not captured in the current feature set.

## Future Improvements

- Incorporate additional vehicle features such as transmission type (Manual/Automatic) and number of previous owners.
- Experiment with non-linear regression models (such as Random Forest Regressor or Gradient Boosting) to evaluate predictive performance.
- Add an API endpoint for programmatic valuation requests.
