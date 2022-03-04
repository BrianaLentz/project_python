from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.controllers import users
from flask_app.models.plant import Plant
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

        
# Display Routes
@app.route('/plant/<int:id>')
def one_plant(id):
    data = {
        'id': id
    }
    data = Plant.get_one_plant_with_user(data)
    print('plant', data.img)
    return render_template('one_plant.html', plant=data, user=session)

@app.route('/new')
def new_plant():
    if not session:
        return redirect('/')
    data = {
        'id': session['id']
    }
    return render_template('new_plant.html', user=data)



@app.route('/edit/<int:id>')
def edit_plant(id):
    data = {
        'id': id
    }
    if not session:
        return redirect('/')
    data = Plant.get_one_plant_with_user(data)
    return render_template('edit_plant.html', plant=data, user=session)



# ACTION ROUTES
@app.route('/create/plant', methods=['POST'])
def create_plant():

    if not Plant.validate_plant(request.form):
        return redirect('/new')
    data = {
        'img': request.files['img'].read(),
        'scientific_name': request.form['scientific_name'],
        'nickname': request.form['nickname'],
        'health': request.form['health'],
        'notes': request.form['notes'],
        'user_id': session['id']
    }

    Plant.save(data)
    return redirect('/hub/'+str(session['id']))


@app.route('/edit/plant/<int:id>', methods=['POST'])
def update_plant(id):
    if not Plant.validate_plant(request.form):
        return redirect('/edit/'+str(id))
    data = {
        'id': id,
        'img': request.files['img'].read(),
        'scientific_name': request.form['scientific_name'],
        'nickname': request.form['nickname'],
        'health': request.form['health'],
        'notes': request.form['notes'],
    }
    Plant.update(data)
    return redirect('/plant/'+str(id))

@app.route('/delete/<int:id>') 
def delete(id):
    data = {
        'id': id,
    }
    Plant.delete(data)
    return redirect('/hub/'+str(session['id']))