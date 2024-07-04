from flask import Blueprint, render_template, request, jsonify, redirect, jsonify
import requests
from datetime import datetime
from markupsafe import escape
from app.blueprints.land_predict.land_predict import lp
from flask_restful import Api, Resource
import pandas as pd
from app import model, db
from flask import session, flash, url_for
from app.blueprints.auth.models.Admin import Admin
api = Api(lp)

def admin_name():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    
    admin_name = db.session.execute(db.select(Admin).filter_by(id=session['id'])).scalar_one()
    return admin_name

@lp.route('/real-time-data', methods=['GET', 'POST'])
def real_time_data():
    if request.method == 'POST':
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        # Convert to datetime objects
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")

        # Format dates in the expected format "%Y-%m-%d %H:%M"
        start_date_formatted = start_date_obj.strftime("%Y-%m-%d %H:%M")
        end_date_formatted = end_date_obj.strftime("%Y-%m-%d %H:%M")
        
        api_data = f"https://alimhidayat.pythonanywhere.com/real-time/dataApi2?start_date={start_date_formatted}&end_date={end_date_formatted}"
        headers = {'Accept': 'application/json'}  # mengatur header request
        response = requests.get(api_data, headers=headers)
        
        date = {
            "start_date": start_date_formatted,
            "end_date": end_date_formatted
        }
        if response.status_code == 200:
            data = response.json()
            return render_template('pre_content/result/real_time.html', data=data, admin_name=admin_name(), date=date)
        else:
            return jsonify({'error': 'Gagal mengambil data'}), 500
    return render_template('pre_content/real_time_data.html', data={}, admin_name=admin_name())


# @lp.route('/real-time-data/stage/<alghoritm>/')
# def real_time_data_stage(alghoritm, ):
#     return render_template('pre_content/result/real_time.html', data=data, admin_name=admin_name(), date=date)
    

@lp.route('/real-time-data/predicted', methods=['GET', 'POST'])
def real_time_data_predict():
    # mengambil nilai dari url parameter
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # mengambil data dari API
    api_data = f"https://alimhidayat.pythonanywhere.com/real-time/dataApi2?start_date={start_date}&end_date={end_date}"
    headers = {'Accept': 'application/json'}  # mengatur header request
    response = requests.get(api_data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # json to dataframe
        dataset = pd.DataFrame(data)
        # predict data
        # drop timestamp and id_realtime column
        dataset_test = dataset.drop(columns=['timeStamp', 'id_realtime'])
        dataset_test = dataset_test.rename(columns={
            'soil_nitro': 'soil_nitro1',
            'soil_ph': 'soil_ph1',
            'soil_phos': 'soil_phos1',
            'soil_pot': 'soil_pot1',
            'soil_temp': 'soil_temp1'
        })
        # urutan kolom harus sama dengan kolom yang digunakan pada saat training
        dataset_test = dataset_test[['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp']]
        
        
        # dataset_test = dataset.drop(columns=['timeStamp'])
        # predict data
        prediction = model.predict(dataset_test)
        # add prediction column before timestamp column
        dataset['nilai_prediksi'] = prediction
        # mengubah urutan kolom 
        
        dataset = dataset[['hum', 'soil_nitro', 'soil_phos', 'soil_pot', 'soil_temp', 'soil_ph', 'temp', 'nilai_prediksi','timeStamp']]
        print(dataset)
        # mengubah menjadi json
        dataset = dataset.to_dict(orient='records')
        return render_template('pre_content/result/result_real_time.html', admin_name=admin_name(), data=dataset)
    else:
        return jsonify({'error': 'Gagal mengambil data'}), 500
    
    
    # dataset = dataset.to_dict()
    
    # df = pd.DataFrame(dataset)
    # print("INI DATAFRAME")
    # print(df)
    # return dataset
    # # print(parameters)
    # parameters = request.args
    # # merubah immutable dict menjadi mutable dict
    # parameters = parameters.to_dict()
    # columns = ['hum', 'soil_nitro1', 'soil_phos1', 'soil_pot1', 'soil_temp1', 'soil_ph1', 'temp']
    # values = [float(parameters['hum']), float(parameters['soil_nitro2']), float(parameters['soil_phos2']), float(parameters['soil_pot2']), float(parameters['soil_temp2']), float(parameters['soil_ph2']), float(parameters['temp'])]
    # parameters = dict(zip(columns, values))
    # data_test = pd.DataFrame(parameters, index=[0])
    # prediction = model.predict(data_test)
    # data_test['Nilai Prediksi'] = prediction
    # return render_template('pre_content/result/result_real_time.html', data=data_test.to_json(orient='records'), admin_name=admin_name())