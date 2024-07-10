from flask import Blueprint, render_template, request, jsonify, redirect, jsonify
import requests
from datetime import datetime
from markupsafe import escape
from app.blueprints.land_predict.land_predict import lp
from flask_restful import Api, Resource
from matplotlib.figure import Figure
import pandas as pd
from app import model, model_dt, model_rf, db
from flask import session, flash, url_for
import base64
from io import BytesIO
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
        alghoritm = request.form['alghoritm']
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        # Convert to datetime objects
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")

        # Format dates in the expected format "%Y-%m-%d %H:%M"
        start_date_formatted = start_date_obj.strftime("%Y-%m-%d %H:%M")
        end_date_formatted = end_date_obj.strftime("%Y-%m-%d %H:%M")
        
        api_data = f"https://flask-selaawi-api.vercel.app/real-time/dataApi2?start_date={start_date_formatted}&end_date={end_date_formatted}"
        headers = {'Accept': 'application/json'}  # mengatur header request
        response = requests.get(api_data, headers=headers)
        
        date = {
            "start_date": start_date_formatted,
            "end_date": end_date_formatted
        }
        # return api_data
        if response.status_code == 200:
            data = response.json()
            # return "nilai"
            # return api_data
            return render_template('pre_content/result/real_time.html', data=data, admin_name=admin_name(), alghoritm=alghoritm, date=date)
        else:
            return jsonify({'error': 'Gagal mengambil data'}), 500
    return render_template('pre_content/real_time_data.html', data={}, admin_name=admin_name())


# @lp.route('/real-time-data/stage/<alghoritm>/')
# def real_time_data_stage(alghoritm, ):
#     return render_template('pre_content/result/real_time.html', data=data, admin_name=admin_name(), date=date)
    

@lp.route('/real-time-data/predicted/<alghoritm>', methods=['GET', 'POST'])
def real_time_data_predict(alghoritm):
    # mengambil nilai dari url parameter
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # mengambil data dari API
    api_data = f"https://flask-selaawi-api.vercel.app/real-time/dataApi2?start_date={start_date}&end_date={end_date}"
    print("INI API_DATA")
    print(api_data)
    headers = {'Accept': 'application/json'}  # mengatur header request
    response = requests.get(api_data, headers=headers)
    print(response)
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
        
        if alghoritm == 'knn':
            prediction = model.predict(dataset_test)
        elif alghoritm == 'rf':
            prediction = model_rf.predict(dataset_test)
        else: 
            prediction = model_dt.predict(dataset_test)
        # add prediction column before timestamp column
        dataset['nilai_prediksi'] = prediction
        # mengubah urutan kolom 
        
        dataset = dataset[['hum', 'soil_nitro', 'soil_phos', 'soil_pot', 'soil_temp', 'soil_ph', 'temp', 'nilai_prediksi','timeStamp']]
        rows, cols = dataset.shape
        # menghitung jumlah nilai prediksi
        x = dataset['nilai_prediksi'].value_counts()
        nilai_tidak = 0 if 'Tidak' not in x.index else dataset['nilai_prediksi'].value_counts()['Tidak']
        nilai_cocok = 0 if 'Cocok' not in x.index else dataset['nilai_prediksi'].value_counts()['Cocok']
        
        fig = Figure()
        ax = fig.subplots()
        color = (232/255, 106/255, 51/255, 1)
        
        labels = x.index.tolist()
        values = [x[val] for val in labels]
        
        if len(x.index) > 1:
            color = ((232/255, 106/255, 51/255, 1), (51/255, 106/255, 232/255, 1))
        ax.bar(labels, values, color=color, label=labels)
        
        ax.set_ylabel("Jumlah Data")
        ax.set_xlabel("Label Prediksi")
        ax.yaxis.grid(True, color='#EEEEEE')
        ax.xaxis.grid(False)
        ax.legend(title='Index Prediksi', loc='upper right')
        
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the htl output
        data_img = base64.b64encode(buf.getbuffer()).decode("ascii")
        # mengubah menjadi json
        dataset = dataset.to_dict(orient='records')
        print(admin_name.image_file)
        return "memanggil"
        return render_template('pre_content/result/result_real_time.html',admin_name=admin_name(), img=data_img ,data=dataset, dimension=[rows, cols], nilai_tidak=nilai_tidak, nilai_cocok=nilai_cocok, alghoritm=alghoritm)
    else:
        return jsonify({'error': 'Gagal mengambil data'}), 500