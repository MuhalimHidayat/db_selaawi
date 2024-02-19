from flask import render_template, redirect, url_for, request, session

from app import app 

@app.route('/')
def index():
    return render_template('user/halaman_awal.html')

@app.route('/tabel-result')
def tabel_result():
    return render_template('user/tabel_result.html')

@app.route('/data-sample')
def data_sample():
    return render_template('user/data_sample.html')

@app.route('/predictions')
def predictions():
    return render_template('user/predictions.html')