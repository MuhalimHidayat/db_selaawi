import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from markupsafe import escape

from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from app.blueprints.auth.models.Admin import Admin

auth_bp = Blueprint('auth', __name__, url_prefix='/user-auth')

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
            flash('Password has been reset')
            return redirect(url_for('auth.sign_in'))
        else:
            flash('Password does not match')
            return redirect(url_for('auth.reset_password', id=admin.id))
    return render_template('authen/resetpass.html', title="Reset Password")


with app.app_context():
    db.create_all()