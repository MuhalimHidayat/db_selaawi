import functools
import html

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from markupsafe import escape, Markup
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app import model, app


# UPLOAD_FOLDER = 'app/blueprints/land_predict/static/datasets'
ALLOWED_EXTENSIONS = {'xlsx','csv'}

# masih salah di bagian static_url_path
lp = Blueprint('land_predict', __name__, url_prefix='/land_predict', static_folder='static', static_url_path='blueprints/land_predict/static')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@lp.route('/add-manual-data', methods=('GET', 'POST'))
def add_manual_data():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    if request.method == 'POST':
        humidity = float(escape(request.form['humidity']))
        nitro = float(escape(request.form['nitro']))
        phosphor = float(escape(request.form['phosphor']))
        pottalium = float(escape(request.form['pottalium']))
        soil = float(escape(request.form['soil']))
        ph = float(escape(request.form['ph']))
        temperature = float(escape(request.form['temperature']))

        data = [[humidity, nitro, phosphor, pottalium, soil, ph, temperature]]
        columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp']
        data_test = pd.DataFrame(data, columns=columns)
        prediction = model.predict(data_test)
        data_test['prediction'] = prediction
        # print("PREDIKSI: ",prediction)
        # nilai akurasinya 
        prediction_data = data_test.to_html(index=False, classes='table-auto', table_id='prediction_results')
        flash("data berhasil di prediksi", "success")
        # kodingan untuk menampilkan hasil prediksi
        return render_template('pre_content/result/manual_data.html', prediction_data=Markup(prediction_data), prediction = prediction)
    # kodingan untuk menampilkan form input data
    return render_template('pre_content/add_manual_data.html', prediction="Belum Memasukkan Data")

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
    
