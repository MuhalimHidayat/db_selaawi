from app.blueprints.land_predict.land_predict import lp
from flask import session, flash, redirect, url_for, request, render_template
from markupsafe import escape
from app.blueprints.land_predict.models.Area import Area
from app.blueprints.land_predict.models.ManualData import ManualData
from sqlalchemy.orm.exc import NoResultFound
import pandas as pd
from app import model, app, db
# manual data


# add-manual_data/area
@lp.route('/add-manual-data/add-area/<int:id_m>', methods=('GET', 'POST'))
def add_area(id_m):
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    if request.method == 'POST':
        latitude = escape(request.form['latitude'])
        longitude = escape(request.form['longitude'])
        # area_name didapatkan dari tabel manual data kolom area
        area_name = ManualData.query.filter_by(id_m=id_m).first().area
        
        add_area = Area(area_name=area_name,area_longitude=longitude,area_latitude=latitude,id=id_m)
        try:
            area_exist = db.session.execute(db.select(Area).filter_by(id=id_m)).scalar_one()
            area_exist.area_longitude = longitude
            area_exist.area_latitude = latitude
        except NoResultFound: 
            db.session.add(add_area)
            
        db.session.commit()
        return redirect(url_for('land_predict.stage_manual_data'))
        # return redirect(url_for('land_predict.result_manual_data', dataset=data_test.to_json(orient='records')))
        # return render_template('pre_content/result/manual_data.html', data_test=data_test, id_m=id_m)
    try:
        area_exist = db.session.execute(db.select(Area).filter_by(id=id_m)).scalar_one()
        return render_template('pre_content/area_result/add_area.html', area_exist=area_exist)
    except NoResultFound:
        return render_template('pre_content/area_result/add_area.html', area_exist='')