from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import random
import tensorflow as tf

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

@app.route('/')
def index():
    return render_template('login.html')

global message
global tossResult 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    global currUser
    user = db.users.find_one({'email': email})
    print(db.users.find_one({'email': email}))
    currUser = user['username']
    
    if user and user['password'] == password:
        message = 'Login successful!'
        return render_template('home.html')
    
    else:
        message = 'Invalid email or password.'
        return redirect(url_for('register'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    iuser = db.users.find_one({'email': email})
    if iuser and iuser['username']:
        message = "Username already exists"
        return render_template('register.html', message = message)

    if username and email and password:
        user = {'username': username, 'email': email, 'password': password}
        db.users.insert_one(user)
        message = 'Registration successful!'
        return redirect(url_for('login'))
        
    else:
        message = 'Please fill in all fields.'

    return render_template('register.html', message = message)

@app.route('/check_up')
def checkUp():
    return render_template('checkUp.html')

@app.route('/predict_common', methods=['POST'])
def predictCommon():
    disease = request.form['disease']
    model = tf.keras.models.load_model('rnn_disease.h5')

    # Perform predictions using the model
    predictions = model.predict(disease)
    
    return render_template('checkUp.html', message=predictions, description=disease)

@app.route('/advanced')
def advanced():
    return render_template('advanced.html')

@app.route('/skin')
def skin():
    return render_template('skin.html')

@app.route('/skinPredict', methods=['POST'])
def skinPredict():
    image = request.form['image']
    model = tf.keras.models.load_model('SKIN_CANER_PREDICTION.h5')

    # Perform predictions using the model
    predictions = model.predict(image)
    
    return render_template('skin.html', message=predictions, image=image)    

@app.route('/profile')
def profile():
    userNameProfile = db.users.find_one({'username': currUser})
    email = userNameProfile['email']
    
    return render_template('profile.html', username=currUser, email=email)


if __name__ == '__main__':
    app.run()
