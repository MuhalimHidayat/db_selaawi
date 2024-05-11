import os
from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import joblib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
# db.init_app(app)
migrate = Migrate(app, db)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
model = joblib.load('app/blueprints/land_predict/static/ml_model/KNN_model.sav')
model_rf = joblib.load('app/blueprints/land_predict/static/ml_model/KNN_model.sav')
model_dt = joblib.load('app/blueprints/land_predict/static/ml_model/KNN_model.sav')

from app.blueprints.land_predict.land_predict import lp
app.register_blueprint(lp)

@app.route('/download-dataset/<dataset_name>')
def download_dataset(dataset_name):
    dataset_path = os.path.join('blueprints', 'land_predict', 'static', 'datasets')
    return send_from_directory(dataset_path, dataset_name)

from app.blueprints.auth.auth import auth_bp
app.register_blueprint(auth_bp)


from app import routes

if __name__ == '__main__':
    app.run(debug=True)