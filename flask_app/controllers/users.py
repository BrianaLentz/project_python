from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.user import User
from flask_app.models.plant import Plant
from flask_app.controllers import plants
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# DISPLAY ROUTES
@app.route('/')
def display_login_reg():
    if session:
        return redirect('/hub/'+str(session['id']))
    return render_template('login_reg.html')

# not in use right now
# @app.route('/home')
# def home():
#     if not session:
#         return redirect('/')
#     data = {
#         'id': session['id']
#     }
#     return render_template('home.html', users=User.get_all_users_with_all_plants(data))


@app.route('/hub/<int:id>')
def hub(id):
    data = {
        'id': id
    }
    if not session:
        return redirect('/')
    print('HERE')
    return render_template('hub.html',user=User.get_one_user_with_all_plants(data))



# ACTION ROUTES
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_reg(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data ={
        'first_name': request.form['first_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    id = User.save(data)
    session['id'] = id
    return redirect('/hub/'+str(id))


@app.route('/login', methods=['POST'])
def login():
    data = {'email' : request.form['email']}
    user = User.validate_email(data)
    if not user:
        flash("Email provided not valid", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Email/Password provided not valid', 'login')
        return redirect('/')
    session['id'] = user.id
    return redirect('/hub/'+str(user.id))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
