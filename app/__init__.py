import os
from flask import Flask, send_from_directory, render_template
import joblib
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
model = joblib.load('app/blueprints/land_predict/static/ml_model/KNN_model.sav')

from app.blueprints.land_predict.land_predict import lp
app.register_blueprint(lp)

@app.route('/download-dataset/<dataset_name>')
def download_dataset(dataset_name):
    dataset_path = os.path.join('blueprints', 'land_predict', 'static', 'datasets')
    return send_from_directory(dataset_path, dataset_name)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/index')
def index2():
    return render_template('predictions/base.html')
if __name__ == '__main__':
    app.run(debug=True)