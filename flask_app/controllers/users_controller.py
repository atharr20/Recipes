from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users_model import User
from flask_app.models.parties_model import Party
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


@app.route('/')
def home ():
    return render_template('register_login.html')



@app.route('/register_user', methods=['POST'])
def successful_register():

    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    newuser_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    newuser_id=User.Save_User(newuser_data)

    session['user_id']= newuser_id

    return redirect('/dashboard')



@app.route('/login_user', methods=['POST'])
def Login_user():
    login_data = {'email': request.form['email']}
    user_in_db = User.GetUserByEmail(login_data)

    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    
    session['user_id'] = user_in_db.id

    return redirect('/dashboard')


@app.route('/dashboard')
def show_success():
    if 'user_id' not in session:
        return redirect('/')
    one_user = User.GetUserByID ({'id': session['user_id']})

    all_parties = Party.get_all_parties()
    return render_template('dashboard.html', one_user=one_user, all_parties=all_parties)

@app.route('/my_parties')
def Show_MyParties():

    one_user= User.GetMyParties({'user_id': session['user_id']})

    return render_template('my_parties.html', one_user=one_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')