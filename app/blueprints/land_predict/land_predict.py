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
        print("INNI SESSSION", session['id'])
        data = [[humidity, nitro, phosphor, pottalium, soil, ph, temperature]]
        columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp']
        data_test = pd.DataFrame(data, columns=columns)
        data_test_json = data_test.to_json(orient='records')
        # data_test_dataframe = data_test.to_html(index=False, classes='table-auto', table_id='prediction_results')
        # return render_template('pre_content/stage/add_manual.html', data_test2=Markup(data_test_dataframe), data_test=data_test.to_json(orient='records'), data_test_coba=data_test_coba)
        return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json)
        # prediction = model.predict(data_test)
        # data_test['prediction'] = prediction
        # # print("PREDIKSI: ",prediction)
        # # nilai akurasinya 
        # prediction_data = data_test.to_html(index=False, classes='table-auto', table_id='prediction_results')
        # flash("data berhasil di prediksi", "success")
        # # kodingan untuk menampilkan hasil prediksi
        # return render_template('pre_content/result/manual_data.html', prediction_data=Markup(prediction_data), prediction = prediction)
    # kodingan untuk menampilkan form input data
    print("INNI SESSSION", session['id'])
    return render_template('pre_content/add_manual_data.html', prediction="Belum Memasukkan Data")

# mencoba memodelkan data
# @lp.route('/stage-manual-data')
# def stage_manual_data():
#     data = [[12, 13, 14, 15, 12, 11, 12]]
#     columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp']
#     data_test = pd.DataFrame(data, columns=columns)
#     data_test_coba = pd.DataFrame(data, columns=columns)
#     data_test_json = data_test.to_json(orient='records')
#     return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json=data_test_json)

@lp.route('/update-manual-data/<dataset>', methods=['GET', 'POST'])
def update_manual_data(dataset):
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    
    data_test_coba = pd.read_json(dataset, orient='records')

    if request.method == 'POST':
        print("NILAI AKHIR INI HARUS ADA")
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
        data_test_json = data_test.to_json(orient='records')
        # data_test_dataframe = data_test.to_html(index=False, classes='table-auto', table_id='prediction_results')
        # return render_template('pre_content/stage/add_manual.html', data_test2=Markup(data_test_dataframe), data_test=data_test.to_json(orient='records'), data_test_coba=data_test_coba)
        return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json)
    return render_template('pre_content/update_manual_data.html', dataset=dataset)

@lp.route('/result-manual-data/<dataset>', methods=('GET', 'POST'))
def result_manual_data(dataset):
    data_test_execute = pd.read_json(dataset, orient='records')
    prediction = model.predict(data_test_execute)
    data_test_execute['prediction'] = prediction
    prediction_data = data_test_execute.to_html(index=False, classes='table-auto', table_id='prediction_results')
    flash("data berhasil di prediksi", "success")
    return render_template('pre_content/result/manual_data.html', prediction_data=Markup(prediction_data), prediction = prediction)

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

