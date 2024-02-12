import os
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from markupsafe import escape
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from app.blueprints.auth.models.Admin import Admin

import hashlib
import time

ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg', 'gif'}

auth_bp = Blueprint('auth', __name__, url_prefix='/user-auth')
app.config['UPLOAD_FOLDER'] = 'app/static/img/uploads'

@auth_bp.route('/')
def authen():
    return render_template('auth.html')

@auth_bp.route('/sign-up', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        username = escape(request.form['username'])
        email = escape(request.form['email'])
        # if password less than 8 characters
        if len(request.form['password']) < 8:
            flash('Password must be at least 8 characters.')
            return redirect(url_for('auth.sign_up'))
        password = generate_password_hash(escape(request.form['password']))
        # if username or password is same as the previous one
        if db.session.query(Admin).filter(Admin.username == username).first() is not None:
            flash(f'Username {username} is already registered.')
            return redirect(url_for('auth.sign_up'))
        
        admin = Admin(username=username, email=email, password_hash=password)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('auth.sign_in'))

    return render_template('authen/signup.html', title='Sign Up')

@auth_bp.route('/sign-in', methods=('GET', 'POST'))
def sign_in():
    if 'id' in session:
        flash('You are already logged in.')
        return redirect(url_for('land_predict.add_manual_data'))
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        # jika username tidak ada maka tidak bisa login
        admin = db.session.query(Admin).filter(Admin.username == username).first() 
        print("Ini user: ", admin.id)
        if admin is None:
            flash('Incorrect username.')
            return redirect(url_for('auth.sign_in'))
        else: 
            # print(check_password_hash(admin.password_hash, password))   
            if check_password_hash(admin.password_hash, password) == False:
                flash('Incorrect password.')
                return redirect(url_for('auth.sign_in'))
            else: 
                # add session 
                session['id'] = admin.id
                return redirect(url_for('land_predict.add_manual_data'))
    return render_template('authen/signin.html', title='Sign In')

@auth_bp.route('/all-user')
def all_user():
    admin = db.session.execute(db.select(Admin).order_by(Admin.username)).scalars()
    
    return render_template('authen/alluser.html', user=admin)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = escape(request.form['username'])
        admin = db.session.query(Admin).filter(Admin.username == username).first()
        if admin is None:
            flash('Incorrect username')
            return redirect(url_for('auth.forgot_password'))
        else: 
            return redirect(url_for('auth.reset_password', id=admin.id))

    return render_template('authen/forgotpass.html', title="Forgot Password")

@auth_bp.route('/reset-password/<int:id>', methods=['GET', 'POST'])
def reset_password(id):
    if request.method == 'POST':
        password = escape(request.form['password'])
        password_confirm = escape(request.form['password_confirm'])

        admin = db.get_or_404(Admin, id)
        if len(password) < 8:
            flash('Password must be at least 8 characters.')
            return redirect(url_for('auth.reset_password', id=admin.id))
        
        if password == password_confirm: 
            admin.password_hash = generate_password_hash(password)
            admin.verified = True
            db.session.commit()
            flash('Password has been reset')
            return redirect(url_for('auth.sign_in'))
        else:
            flash('Password does not match')
            return redirect(url_for('auth.reset_password', id=admin.id))
    return render_template('authen/resetpass.html', title="Reset Password")

# settings = change profile, change username, change email and upload profile photo
@auth_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.sign_in'))
    admin = db.get_or_404(Admin, session['id'])
    if request.method == 'POST':
        username = escape(request.form['username'])
        email = escape(request.form['email'])
        

        if db.session.query(Admin).filter(Admin.username == username).first() is not None or db.session.query(Admin).filter(Admin.email == email).first() is not None:
            if (username == admin.username or email == admin.email):
                flash('Username or email has not been changed.')
                # ini harus tetep jalan dan bisa merubah
                admin.username = username
                admin.email = email
                admin.image_file = upload_photo(request.files['image_file'])
                admin.verified = True
                db.session.commit()
                # print(username)
                # print(email)
                # print(upload_photo(request.files['image_file']))
                flash('Berhasil Mengubah database')
                return redirect(url_for('auth.settings'))
                # berhasil
            else: 
                flash('Username or email has been used')
                return redirect(url_for('auth.settings'))

        # berhasil 
        admin.username = username
        admin.email = email
        admin.image_file = upload_photo(request.files['image_file'])
        admin.verified = True
        db.session.commit()
        # print(username)
        # print(email)
        # print(upload_photo(request.files['image_file']))
        # flash messege
        flash('Berhasil Mengubah database')
        return redirect(url_for('auth.settings'))
    return render_template('authen/settings.html', title="Settings", admin=admin)
        # upload photo

# upload file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS_IMG
def upload_photo(image_file):
    last_image = request.form['last_image']
    # if dibawah ini digunakan untuk mengambil file yang diupload JIKA ada file yang diupload 
    if 'image_file' not in request.files:
        flash('No file part', 'danger')
        # return redirect(request.url)
        return last_image
    file = image_file
    if file.filename == '':
        flash('No selected file', 'danger')
        return last_image
    if file and allowed_file(file.filename):
        # make a unique name for the file
        filename = secure_filename(file.filename)
        filename_hash = hashlib.md5((filename + str(time.time())).encode('utf-8')).hexdigest()
        extension = filename.rsplit('.', 1)[-1].lower()
        filename_hash += '.' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_hash))
        return filename_hash
    return last_image
# delete profile
@auth_bp.route('/delete')
def delete():
    admin = db.get_or_404(Admin, session['id'])
    session.clear()
    flash(f'Username {admin.username} has been deleted.')
    db.session.delete(admin)
    db.session.commit()
    return redirect(url_for('auth.sign_up'))


# logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('auth.sign_in'))

with app.app_context():
    db.create_all()