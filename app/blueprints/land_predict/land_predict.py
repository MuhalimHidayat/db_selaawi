import functools
import html

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from markupsafe import escape, Markup
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app.blueprints.land_predict.models.ManualData import ManualData
from app import model, app, db


# UPLOAD_FOLDER = 'app/blueprints/land_predict/static/datasets'
ALLOWED_EXTENSIONS = {'xlsx','csv'}

# masih salah di bagian static_url_path
lp = Blueprint('land_predict', __name__, url_prefix='/land_predict', static_folder='static', static_url_path='blueprints/land_predict/static')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# @lp.route('/add-manual-data', methods=['GET', 'POST'])
# def add_manual_dataa():
#     if 'id' not in session: 
#         flash('You must be logged in to access this page', 'danger')
#         return redirect(url_for('auth.sign_in'))

# mengambil seluruh yang ada pada file add_manual_data
from app.blueprints.land_predict import add_manual_data


# dataset upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@lp.route('/add-dataset', methods=('GET', 'POST'))
def add_dataset():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    if request.method == 'POST':
        if 'dataset' not in request.files:
            flash('No file part', "danger")
            return redirect(request.url)
        file = request.files['dataset']
        if file.filename == '':
            flash('No selected file', "danger")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # MACHINE LEARNING MODEL HERE
            df = pd.read_excel(request.files['dataset'])
            X = df.iloc[:, :-1]
            prediction = model.predict(X)
            df['prediction'] = prediction
            # df.to_excel(UPLOAD_FOLDER+'/'+filename)
            df.to_excel('app/blueprints/land_predict/static/datasets/'+filename, index=False)
            # file.save(UPLOAD_FOLDER+'/'+filename)
            prediction_data = df.to_html(index=False, classes='table-auto', table_id='prediction_results')
            rows = len(df.axes[0])
            cols = len(df.axes[1])
            flash('File berhasil di upload', "success")
            # return render_template('add_dataset.html', prediction="berhasil di prediksi", dataset=download_dataset(filename))
            # return render_template('pre_content/add_dataset.html', dataset_name=filename)
            return render_template('pre_content/result/dataset.html', dataset_name=filename, prediction_data=Markup(prediction_data), dimensions=[rows, cols])
        return render_template('pre_content/add_dataset.html')
    return render_template('pre_content/add_dataset.html')

# download dataset

@lp.route('/input-manual-data')
def input_manual_data():
    # manual_data = ManualData(hum=0.5, soil_nitro1=0.5, soil_phos1=0.5, soil_pot1=0.5, temp=0.5, prediction='Tidak Tahu', id=1)
    manual_data = ManualData(hum=0.5, soil_nitro1=0.5, soil_phos1=0.5, soil_pot1=0.5, temp=0.5, prediction='Tidak Tahu', id=1)
    # manual_data = "Nilai ini diambil dari database."
    # return "<h1> Broken Heart</h1>"
    db.session.add(manual_data)
    db.session.commit()
    return render_template('pre_content/add_dataset.html')

@lp.route('/looking-new-data')
def looking_new_data():
    new_manual_data = ManualData(hum=0.5, soil_nitro1=0.5, soil_phos1=0.5, soil_pot1=0.5, temp=0.5, prediction='Tidak Tahu', id=1)
    for data in new_manual_data:
        print(data.hum)
    return render_template('pre_content/add_manual_data.html')

