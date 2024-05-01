from flask import Blueprint, render_template, request, jsonify, redirect
import requests
from markupsafe import escape
from app.blueprints.land_predict.land_predict import lp
from flask_restful import Api, Resource
import pandas as pd

api = Api(lp)

@lp.route('/real-time-data', methods=['GET', 'POST'])
def real_time_data():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        slave = request.form['slave']
        if slave == 'slave-2':
            slaveData = '3'
        else:
            slaveData = '2'
        try:
            api_data_area001 = f"https://sems-webservice-ten.vercel.app/api/sensor/avg?area=AREA001&start_date={start_date}&end_date={end_date}"
            # api_data_area001 = "https://sems-webservice-ten.vercel.app/api/sensor/avg?area=AREA001&start_date=2024-04-27&end_date=2024-04-28"
            if slave == 'slave-1':
                api_data_area002_003 = f"https://sems-webservice-ten.vercel.app/api/sensor/avg?area=AREA002&start_date={start_date}&end_date={end_date}"
            else: 
                api_data_area002_003 = f"https://sems-webservice-ten.vercel.app/api/sensor/avg?area=AREA003&start_date={start_date}&end_date={end_date}"   
            headers = {'Accept': 'application/json'}  # mengatur header request
            response_area001 = requests.get(api_data_area001, headers=headers)  # mengirim request ke API (endpoint: /api/v1/employees
            response_area002_003 = requests.get(api_data_area002_003, headers=headers)  # mengirim request ke API (endpoint: /api/v1/employees
            if response_area001.status_code == 200 and response_area002_003.status_code == 200:
                data_area001 = response_area001.json() # mengambil data JSON dari API
                data_area002_003 = response_area002_003.json() # mengambil data JSON dari API
                data = {
                    'area001': data_area001,
                    f'area00{slaveData}': data_area002_003
                }
                return render_template('pre_content/result/real_time.html', data=data, slave_data = slave)
                # return jsonify(data)
            else:
                return jsonify({'error': 'Gagal mengambil data'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template('pre_content/real_time_data.html', data={})

@lp.route('/real-time-data/predicted', methods=['GET', 'POST'])
def real_time_data_predict():
    # print(parameters)
    parameters = request.args
    # merubah immutable dict menjadi mutable dict
    parameters = parameters.to_dict()
    data_test = pd.DataFrame(parameters, index=[0])
    print(data_test)
    return "nilai berganti"
    
    



@lp.route('/real-time-data/bencana')
def result():
    slave_data = 'slave-2'
    api_data_area001 = f"https://sems-webservice-ten.vercel.app/api/sensor/avg?area=AREA001&start_date=2024-04-28&end_date=2024-04-29"
    api_data_area002_003 = f"https://sems-webservice-ten.vercel.app/api/sensor/avg?area=AREA003&start_date=2024-04-28&end_date=2024-04-29"
    headers = {'Accept': 'application/json'}  # mengatur header request
    response_area001 = requests.get(api_data_area001, headers=headers)
    response_area002_003 = requests.get(api_data_area002_003, headers=headers)
    if response_area001.status_code == 200 and response_area002_003.status_code == 200:
        data_area001 = response_area001.json()
        data_area002_003 = response_area002_003.json()
        data = {
            'area001': data_area001,
            'area002_003': data_area002_003
        }
        return render_template('pre_content/result/real_time.html', data=data, slave_data = slave_data)
    else:
        return jsonify({'error': 'Gagal mengambil data'}), 500
    