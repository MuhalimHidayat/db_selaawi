import functools
import html

from flask import (
    flash, g, redirect, render_template, request, session, url_for, send_from_directory, send_file
)
from markupsafe import escape, Markup
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import desc
import json
from app.blueprints.land_predict.models.ManualData import ManualData
from app.blueprints.land_predict.models.Area import Area
from app.blueprints.auth.models.Admin import Admin
from app import model, model_rf, model_dt, app, db
from matplotlib.figure import Figure
import base64
from io import BytesIO

# mengambil blueprint dari file land_predict.py
from app.blueprints.land_predict.land_predict import lp

def admin_name():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    
    admin_name = db.session.execute(db.select(Admin).filter_by(id=session['id'])).scalar_one()
    return admin_name

@lp.route('/add-manual-data', methods=('GET', 'POST'))
def add_manual_data():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    if request.method == 'POST':
        area = escape(request.form['area'])
        humidity = float(escape(request.form['humidity']))
        nitro = float(escape(request.form['nitro']))
        phosphor = float(escape(request.form['phosphor']))
        pottalium = float(escape(request.form['pottalium']))
        soil = float(escape(request.form['soil']))
        ph = float(escape(request.form['ph']))
        temperature = float(escape(request.form['temperature']))
        # print("INNI SESSSION", session['id'])
        # memasukan data area ke tabel Area
        
        # memasukan data kedalam database ke tabel ManualData
        input_manual_data = ManualData(area=area, hum=humidity, soil_nitro1=nitro, soil_phos1=phosphor, soil_pot1=pottalium, soil_temp1=soil, soil_ph1=ph, temp=temperature, id=session['id'])
        # jika berhasil melakukan input data ke database maka akan di commit jika tidak maka akan di rollback
        try:
            db.session.add(input_manual_data)
            db.session.commit()
        except:
            # flash("Data gagal di input", "danger")
            # print("data gagal di masukan")
            return redirect(url_for('land_predict.add_manual_data'))
        
        
        # mengambil semua data yang ada pada database dengan id sama dengan session id
        data_input = ManualData.query.filter_by(id=session['id']).order_by(desc(ManualData.id_m)).all()
        data_array = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in data_input]
        
        data_input_manual = []
        for data in data_array:
            data_input_manual.append([data['hum'], data['soil_nitro1'], data['soil_phos1'], data['soil_pot1'], data['soil_temp1'], data['soil_ph1'], data['temp'], data['id_m']])

        data = data_input_manual
        columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp', 'id_m']
        data_test = pd.DataFrame(data, columns=columns)
        # return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json)
        return redirect(url_for('land_predict.stage_manual_data'))
    return render_template('pre_content/add_manual_data.html', prediction="Belum Memasukkan Data", admin_name=admin_name())

# debug untuk halaman add_manual_data
# mencoba memodelkan data
@lp.route('/stage-manual-data', methods=['GET', 'POST'])
def stage_manual_data():
    # return "Nilai"
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    # data_input = ManualData.query.filter_by(id=session['id']).all() #also order by id_m desc
    # data_input = db.select(ManualData).filter_by(id=session['id']).order_by(desc(ManualData.id_m))

    data_input = ManualData.query.filter_by(id=session['id']).order_by(desc(ManualData.id_m)).all()
    data_array = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in data_input]
    print(data_array)
    data_input_manual = []
    for data in data_array:
        data_input_manual.append([data['area'], data['hum'], data['soil_nitro1'], data['soil_phos1'], data['soil_pot1'], data['soil_temp1'], data['soil_ph1'], data['temp'], data['id_m']])

    data = data_input_manual
    columns = ['area','hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp', 'id_m']
    data_test = pd.DataFrame(data, columns=columns)
    
    # fetching area
    statement = db.select(Area).join(ManualData, ManualData.id_m == Area.id).filter(ManualData.id == session['id'])
    area = db.session.execute(statement).scalars()
    area = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in area]
    area = pd.DataFrame(area)
    area = area.to_json(orient='records')
    
    if request.method == 'POST':
        alghoritm = request.form['alghrotim']
        return redirect(url_for('land_predict.result_manual_data', alghoritm=alghoritm ,dataset=data_test.to_json(orient='records') ))
    return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), area=area, admin_name=admin_name())


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
        area = escape(request.form['area'])
        humidity = float(escape(request.form['humidity']))
        nitro = float(escape(request.form['nitro']))
        phosphor = float(escape(request.form['phosphor']))
        pottalium = float(escape(request.form['pottalium']))
        soil = float(escape(request.form['soil']))
        ph = float(escape(request.form['ph']))
        temperature = float(escape(request.form['temperature']))

        # melakukan update data pada database
        update_manual_data = ManualData.query.filter_by(id_m=id_m).first()
        update_manual_data.area = area
        update_manual_data.hum = humidity
        update_manual_data.soil_nitro1 = nitro
        update_manual_data.soil_phos1 = phosphor
        update_manual_data.soil_pot1 = pottalium
        update_manual_data.soil_temp1 = soil
        update_manual_data.soil_ph1 = ph
        update_manual_data.temp = temperature
        # melakukan update data nama area pada tabel Area
        update_area = Area.query.filter_by(id=id_m).first()
        update_area.area_name = area
        db.session.commit()
        flash("Data berhasil di update", "success")

        datadata = ManualData.query.filter_by(id=session['id']).all()
        data_array = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in datadata]
        
        data_input_manual = []
        for data in data_array:
            data_input_manual.append([data['area'],data['hum'], data['soil_nitro1'], data['soil_phos1'], data['soil_pot1'], data['soil_temp1'], data['soil_ph1'], data['temp'], data['id_m']])
        # return redirect(url_for('land_predict.stage_manual_data'))
        data = data_input_manual
        columns = ['area','hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp', 'id_m']
        data_test = pd.DataFrame(data, columns=columns)
        data_test_json = pd.DataFrame(data, columns=columns)
        return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json.to_json(orient='records'), admin_name=admin_name())
    
    return render_template('pre_content/update_manual_data.html', data_input=data_test.to_json(orient='records'), admin_name=admin_name())


@lp.route('/update-manual-data/<dataset>', methods=['GET', 'POST'])
def update_manual_data2(dataset):
    print(dataset)
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
        data_test_json = data_test.to_json(orient='records')
        # data_test_dataframe = data_test.to_html(index=False, classes='table-auto', table_id='prediction_results')
        # return render_template('pre_content/stage/add_manual.html', data_test2=Markup(data_test_dataframe), data_test=data_test.to_json(orient='records'), data_test_coba=data_test_coba)
        return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json, admin_name=admin_name())
    return render_template('pre_content/update_manual_data.html', dataset=dataset, admin_name=admin_name())

@lp.route('/delete-manual-data/')
def delete_manual_data():
    id_m = request.args.get('id_m')

    Area.query.filter_by(id=id_m).delete()
    delete_data = db.get_or_404(ManualData, id_m, description="Data not found")
    db.session.delete(delete_data)
    
    db.session.commit()
    
    data_input = ManualData.query.filter_by(id=session['id']).all()
    data_array = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in data_input]
    # print(data_array)
    data_input_manual = []
    for data in data_array:
        data_input_manual.append([data['area'], data['hum'], data['soil_nitro1'], data['soil_phos1'], data['soil_pot1'], data['soil_temp1'], data['soil_ph1'], data['temp'], data['id_m']])

    data = data_input_manual
    columns = ['area','hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp', 'id_m']
    data_test = pd.DataFrame(data, columns=columns)
    data_test_coba = pd.DataFrame(data, columns=columns)
    data_test_json = data_test.to_json(orient='records')
    # return render_template('pre_content/stage/add_manual.html', data_test=data_test.to_json(orient='records'), data_test_json = data_test_json, admin_name=admin_name())
    return redirect(url_for('land_predict.stage_manual_data'))

@lp.route('/result-manual-data/<alghoritm>/<dataset>', methods=('GET', 'POST'))
def result_manual_data(alghoritm, dataset):
    print("ALGORITM", alghoritm)
    data_test_execute = pd.read_json(dataset, orient='records')
    # print(data_test_execute.dtypes)
    # print(data_test_execute.iloc[:, 1:-1])
    if alghoritm == 'rf':
        prediction = model_rf.predict(data_test_execute.iloc[:, 1:-1])
        data_test_execute['prediction'] = prediction
        data_test_execute['prediction'] = data_test_execute['prediction'].apply(lambda x: 'Tidak' if x == 1 else 'Cocok')
        prediction_data = data_test_execute.to_html(index=False, classes='table-auto', table_id='prediction_results')
    elif alghoritm == 'dt':
        prediction = model_dt.predict(data_test_execute.iloc[:, 1:-1])
        # df['prediction'] = df['prediction'].apply(lambda x: 'Tidak' if x == 1 else 'Cocok')
        data_test_execute['prediction'] = prediction
        data_test_execute['prediction'] = data_test_execute['prediction'].apply(lambda x: 'Tidak' if x == 1 else 'Cocok')
        prediction_data = data_test_execute.to_html(index=False, classes='table-auto', table_id='prediction_results')
    else:    
        prediction = model.predict(data_test_execute.iloc[:, 1:-1])
        data_test_execute['prediction'] = prediction
        prediction_data = data_test_execute.to_html(index=False, classes='table-auto', table_id='prediction_results')
    flash("data berhasil di prediksi", "success")
    # return  "coba"
    # SELECT area.area_longitude, area.area_latitude FROM area join manualdata on area.id = manualdata.id_m
    # fungsi filter by id_m = session['id'] maksudnya adalah mengambil data yang memiliki id_m sama dengan session['id']
    statement = db.select(Area).join(ManualData, ManualData.id_m == Area.id).filter(ManualData.id == session['id'])
    area = db.session.execute(statement).scalars()
    # mengambil data dari area kemudian merubah data tersebut supaya bisa menjadi json
    area = [{key: value for key, value in data.__dict__.items() if not key.startswith('_sa_')} for data in area]
    area = pd.DataFrame(area)
    area = area.to_json(orient='records')
    
    x = data_test_execute['prediction'].value_counts()
    print(x)
    
    nilai_tidak = 0 if 'Tidak' not in x.index else data_test_execute['prediction'].value_counts()['Tidak']
    nilai_cocok = 0 if 'Cocok' not in x.index else data_test_execute['prediction'].value_counts()['Cocok']
    
    fig = Figure()
    ax = fig.subplots()
    color = (232/255, 106/255, 51/255, 1)
    
    labels = x.index.tolist()
    values = [x[val] for val in labels]
    
    if len(x.index) > 1:
        color = ((65/255, 100/255, 74/255, 1),(232/255, 106/255, 51/255, 1))
    ax.bar(labels, values, color=color, label=labels)
    
    ax.set_ylabel("Jumlah Data")
    ax.set_xlabel("Label Prediksi")
    # ax.set_title("Persebaran Bawang Merah Berdasarkan Prediksi")
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)
    ax.legend(title='Index Prediksi', loc='upper right')
    
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the htl output
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return render_template('pre_content/result/manual_data.html', prediction_data=Markup(prediction_data), prediction = prediction, data_test = data_test_execute.to_json(orient='records'), area=area, img=data, nilai_tidak=nilai_tidak, nilai_cocok=nilai_cocok, admin_name=admin_name())

@lp.route('/imagesmatplotlib')
def imagesmatplotlib():
    df = pd.read_excel('app/blueprints/land_predict/static/datasets/data_training-2024-05-13-23-08-27-788316.xlsx')
    x = df['prediction'].value_counts()
    print(x)
    fig = Figure()
    ax = fig.subplots()
    nilai_tidak = df['prediction'].value_counts()['Tidak']
    print(nilai_tidak)
    ax.bar(x.index, x.values, color='red')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    
    # return render_template('pre_content/imagesmatplotlib.html')
    
@lp.route('/download-manual-data/<dataset>')
def download_manual_data(dataset):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df = pd.read_json(dataset, orient='records')
    # remove id_m column
    df = df.drop(columns=['id_m'])
    df.to_excel(writer, index=False)
    writer.close()  # Use close instead of save
    
    output.seek(0)
    
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', download_name='data_training.xlsx', as_attachment=True)
    