import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from markupsafe import escape
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
from app import model
# masih salah di bagian static_url_path
lp = Blueprint('land_predict', __name__, url_prefix='/land_predict', template_folder='templates', static_folder='static', static_url_path='/static/land_predict')

@lp.route('/add-manual-data', methods=('GET', 'POST'))
def add_manual_data():
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
        print("PREDIKSI: ",prediction)
        # print(humidity)
        flash("data berhasil di prediksi", "success")
        return render_template('add_manual_data.html', prediction=prediction)
    return render_template('add_manual_data.html', prediction="Belum Memasukkan Data")
