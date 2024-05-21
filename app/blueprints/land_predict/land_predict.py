import functools
import html
import hashlib
import time
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from markupsafe import escape, Markup
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app.blueprints.land_predict.models.ManualData import ManualData
from app.blueprints.land_predict.models.Dataset import Dataset
from app.blueprints.land_predict.models.Area import Area
from app import model, model_dt, model_rf, app, db
from sqlalchemy import desc
from datetime import datetime


# UPLOAD_FOLDER = 'app/blueprints/land_predict/static/datasets'
ALLOWED_EXTENSIONS = {'xlsx','csv'}

# masih salah di bagian static_url_path
lp = Blueprint('land_predict', __name__, url_prefix='/land_predict', static_folder='static', static_url_path='blueprints/land_predict/static')

# mengambil seluruh yang ada pada file add_manual_data
from app.blueprints.land_predict import add_manual_data, real_time_data, area
from app.blueprints.auth.models.Admin import Admin



@lp.route('/dashboard')
def dashboard():
    if 'id' not in session:
        flash('You must be logged in to access this page','danger')
        return redirect(url_for('auth.sign_in'))
    admin_name = db.session.execute(db.select(Admin).filter_by(id=session['id'])).scalar_one().username
    
    return render_template('pre_content/dashboard.html',admin_name=admin_name)

# dataset upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# latest
def hash_filename(dataset_name, file_name):
    name_inputed = file_name.replace(' ', '_')
    extension = dataset_name.rsplit('.', 1)[-1].lower()
    differentiator_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    name_inputed = name_inputed + '-' + differentiator_name
    name_inputed += '.' + extension
    return name_inputed

@lp.route('/add-dataset', methods=('GET', 'POST'))
def add_dataset():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    if request.method == 'POST':
        if 'dataset' not in request.files:
            flash('No file part', "danger")
            return redirect(request.url)
        dataset = request.files['dataset']
        if dataset.filename == '':
            flash('No selected file', "danger")
            # back to this url again
            return redirect(request.url)
        if dataset and allowed_file(dataset.filename):
            name = escape(request.form['name'])
            dataset_name = secure_filename(dataset.filename)
            dataset_name_hashed = hash_filename(dataset_name, name)
            # doing prediction here,
            df = pd.read_excel(dataset)
            X = df.iloc[:, :-1]
            # pilih algoritma yang akan digunakan
            alghoritm = request.form['alghoritm']
            if alghoritm == 'K-Nearest Neighbors':
                prediction = model.predict(X)
                df['prediction'] = prediction
            elif alghoritm == 'Decision Tree':
                prediction = model_dt.predict(X)
                df['prediction'] = prediction
            else: 
                prediction = model_rf.predict(X)
                df['prediction'] = prediction
                
            df.to_excel('app/blueprints/land_predict/static/datasets/'+dataset_name_hashed, index=False)
            # prediction_data = df.to_html(index=False, classes='table-auto', table_id='prediction_results')
            # rows = len(df.axes[0])
            # cols = len(df.axes[1])
            # end of prediction
            # save to database
            add_dataset = Dataset(file_name=name, file_hash=dataset_name_hashed, prediction=alghoritm ,id=session['id'])
            db.session.add(add_dataset)
            db.session.commit()
            # end of save to database

            flash('File berhasil di upload', "success")
            return redirect(url_for('land_predict.stage_dataset', page=1))
            # return render_template('pre_content/result/dataset.html', prediction_data=Markup(prediction_data), dimensions=[rows, cols])
        flash('File tidak di upload', "danger")
        return render_template('pre_content/add_dataset.html')
    return render_template('pre_content/add_dataset.html')

@lp.route('/stage-dataset/page=<int:page>')
def stage_dataset(page=1):
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    
    # datasets = db.session.execute(db.select(Dataset).filter_by(id=session['id'])).scalars().all()
    datasets = Dataset.query.filter_by(id=session['id']).order_by(desc(Dataset.id_d)).paginate(page=page, per_page=5, error_out=False)
    return render_template('pre_content/stage/dataset.html', datasets=datasets)


@lp.route('/stage-dataset/<int:id>/delete')
def delete_dataset(id):
    # dataset = db.session.execute(db.select(Dataset).filter_by(id=id)).scalar()
    dataset = db.get_or_404(Dataset, id)
    db.session.delete(dataset)
    db.session.commit()
    return redirect(url_for('land_predict.stage_dataset', page=1))


@lp.route('/stage-dataset/<string:file_hash>/download')
def download_dataset(file_hash):
    dataset = db.session.execute(db.select(Dataset).filter_by(file_hash=file_hash)).scalar()
    return send_from_directory('land_predict.static/datasets/', dataset.file_hash, as_attachment=True)

# search 
@lp.route('/stage-dataset/search', methods=['POST'])
def search_dataset():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    page = request.args.get('page')
    search = request.form['keyword']
    datasets = Dataset.query.filter(Dataset.file_name.like('%'+search+'%')).paginate(page=page, per_page=5, error_out=False)
    return render_template('pre_content/stage/dataset.html', datasets=datasets)

@lp.route('/stage-dataset/<string:file_hash>/predict')
def predict_dataset(file_hash):
    dataset = db.session.execute(db.select(Dataset).filter_by(file_hash=file_hash)).scalar()
    df = pd.read_excel('app/blueprints/land_predict/static/datasets/'+dataset.file_hash)
    prediction_data = df.to_html(index=False, classes='table-auto', table_id='prediction_results')
    rows = len(df.axes[0])
    cols = len(df.axes[1])
    return render_template('pre_content/result/dataset.html', prediction_data=Markup(prediction_data), dimensions=[rows, cols], data_test = df.to_json(orient='records'))