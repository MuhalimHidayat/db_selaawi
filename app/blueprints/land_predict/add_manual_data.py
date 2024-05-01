import functools
import html

from flask import (
    flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from markupsafe import escape, Markup
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import desc
import json
from app.blueprints.land_predict.models.ManualData import ManualData
from app import model, app, db

# mengambil blueprint dari file land_predict.py
from app.blueprints.land_predict.land_predict import lp

@lp.route('/ini-coba-ajah')
def ini_coba_ajah():
    return "ini coba ajah"


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
        # print("INNI SESSSION", session['id'])
        # memasukan data kedalam database
        input_manual_data = ManualData(hum=humidity, soil_nitro1=nitro, soil_phos1=phosphor, soil_pot1=pottalium, soil_temp1=soil, soil_ph1=ph, temp=temperature, id=session['id'])
        # jika berhasil melakukan input data ke database maka akan di commit jika tidak maka akan di rollback
        try:
            db.session.add(input_manual_data)
            db.session.commit()
        except:
            # flash("Data gagal di input", "danger")
            print("data gagal di masukan")
            return redirect(url_for('land_predict.add_manual_data'))
        
        
        # mengambil semua data yang ada pada database dengan id sama dengan session id
        data_input = ManualData.query.filter_by(id=session['id']).all()
        data_array = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in data_input]
        
        data_input_manual = []
        for data in data_array:
            data_input_manual.append([data['hum'], data['soil_nitro1'], data['soil_phos1'], data['soil_pot1'], data['soil_temp1'], data['soil_ph1'], data['temp'], data['id_m']])

        data = data_input_manual
        columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp', 'id_m']
        data_test = pd.DataFrame(data, columns=columns)
        print(data_test)
        data_test_json = data_test.to_json(orient='records')
        return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json)
    return render_template('pre_content/add_manual_data.html', prediction="Belum Memasukkan Data")

# debug untuk halaman add_manual_data
# mencoba memodelkan data
@lp.route('/stage-manual-data')
def stage_manual_data():
    data_input = ManualData.query.filter_by(id=session['id']).all()
    data_array = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in data_input]

    data_input_manual = []
    for data in data_array:
        data_input_manual.append([data['hum'], data['soil_nitro1'], data['soil_phos1'], data['soil_pot1'], data['soil_temp1'], data['soil_ph1'], data['temp'], data['id_m']])

    data = data_input_manual
    columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp', 'id_m']
    data_test = pd.DataFrame(data, columns=columns)
    data_test_coba = pd.DataFrame(data, columns=columns)
    data_test_json = data_test.to_json(orient='records')
    return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json=data_test_json)


@lp.route('/update-manual-data/', methods=['GET', 'POST'])
def update_manual_data():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    
    id_m = request.args.get('id_m')
    data_input = db.one_or_404(db.select(ManualData).filter_by(id_m=id_m), description="Data not found")
    data_test = [{key: value for key, value in data_input.__dict__.items() if not key.startswith('_sa_')}]
    data_test = pd.DataFrame(data_test)

    if request.method == 'POST':
        humidity = float(escape(request.form['humidity']))
        nitro = float(escape(request.form['nitro']))
        phosphor = float(escape(request.form['phosphor']))
        pottalium = float(escape(request.form['pottalium']))
        soil = float(escape(request.form['soil']))
        ph = float(escape(request.form['ph']))
        temperature = float(escape(request.form['temperature']))

        # melakukan update data pada database
        update_manual_data = ManualData.query.filter_by(id_m=id_m).first()
        update_manual_data.hum = humidity
        update_manual_data.soil_nitro1 = nitro
        update_manual_data.soil_phos1 = phosphor
        update_manual_data.soil_pot1 = pottalium
        update_manual_data.soil_temp1 = soil
        update_manual_data.soil_ph1 = ph
        update_manual_data.temp = temperature
        db.session.commit()
        flash("Data berhasil di update", "success")

        datadata = ManualData.query.filter_by(id=session['id']).all()
        data_array = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in datadata]
        
        data_input_manual = []
        for data in data_array:
            data_input_manual.append([data['hum'], data['soil_nitro1'], data['soil_phos1'], data['soil_pot1'], data['soil_temp1'], data['soil_ph1'], data['temp'], data['id_m']])
        # return redirect(url_for('land_predict.stage_manual_data'))
        data = data_input_manual
        columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp', 'id_m']
        data_test = pd.DataFrame(data, columns=columns)
        data_test_json = pd.DataFrame(data, columns=columns)
        return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json.to_json(orient='records'))
    
    return render_template('pre_content/update_manual_data.html', data_input=data_test.to_json(orient='records'))


@lp.route('/update-manual-data/<dataset>', methods=['GET', 'POST'])
def update_manual_data2(dataset):
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    
    data_test_coba = pd.read_json(dataset, orient='records')

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
        data_test_json = data_test.to_json(orient='records')
        # data_test_dataframe = data_test.to_html(index=False, classes='table-auto', table_id='prediction_results')
        # return render_template('pre_content/stage/add_manual.html', data_test2=Markup(data_test_dataframe), data_test=data_test.to_json(orient='records'), data_test_coba=data_test_coba)
        return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json)
    return render_template('pre_content/update_manual_data.html', dataset=dataset)

@lp.route('/delete-manual-data/')
def delete_manual_data():
    id_m = request.args.get('id_m')

    delete_data = db.get_or_404(ManualData, id_m, description="Data not found")
    db.session.delete(delete_data)
    db.session.commit()
    
    data_input = ManualData.query.filter_by(id=session['id']).all()
    data_array = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in data_input]
    print(data_array)
    data_input_manual = []
    for data in data_array:
        data_input_manual.append([data['hum'], data['soil_nitro1'], data['soil_phos1'], data['soil_pot1'], data['soil_temp1'], data['soil_ph1'], data['temp'], data['id_m']])

    data = data_input_manual
    columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp', 'id_m']
    data_test = pd.DataFrame(data, columns=columns)
    data_test_coba = pd.DataFrame(data, columns=columns)
    data_test_json = data_test.to_json(orient='records')
    return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json)

@lp.route('/result-manual-data/<dataset>', methods=('GET', 'POST'))
def result_manual_data(dataset):
    data_test_execute = pd.read_json(dataset, orient='records')
    print(data_test_execute.dtypes)
    print(data_test_execute.iloc[:, :-1])
    
    prediction = model.predict(data_test_execute.iloc[:, :-1])
    data_test_execute['prediction'] = prediction
    prediction_data = data_test_execute.to_html(index=False, classes='table-auto', table_id='prediction_results')
    flash("data berhasil di prediksi", "success")
    return render_template('pre_content/result/manual_data.html', prediction_data=Markup(prediction_data), prediction = prediction)

    # print(data_test_execute.iloc[[0, 1, 2, 3, 4, 5, 6]])
    # return "berhasil"