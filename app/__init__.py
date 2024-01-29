from flask import Flask
import joblib
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
model = joblib.load('app/blueprints/land_predict/static/ml_model/KNN_model.sav')

from app.blueprints.land_predict.land_predict import lp
app.register_blueprint(lp)


if __name__ == '__main__':
    app.run(debug=True)