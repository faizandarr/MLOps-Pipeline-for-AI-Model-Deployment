from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import pickle
import pandas as pd
import logging
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # For session management
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Create the database
with app.app_context():
    db.create_all()
    
# Load the trained model
try:
    with open('model.pkl', 'rb') as f: #checking modelfile
        model = pickle.load(f)
except FileNotFoundError:
    logging.error("Model file not found.")
    jsonify({'error': 'Model file not found'}), 500

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400

    # Hash the password and create a new user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_id = data.get('user_id')

    if not user_id or not User.query.get(user_id):
        return jsonify({'error': 'Unauthorized access'}), 401

    try:
        humidity = data['humidity']
        windSpeed = data['windSpeed']

        # Prepare input for the model
        input_data = pd.DataFrame([[humidity, windSpeed]], columns=['Humidity', 'Wind Speed'])

        prediction = model.predict(input_data)[0]
        return jsonify({'temperature': prediction})
    except KeyError as e:
        logging.error(f"Missing key in request: {e}")
        return jsonify({'error': 'Invalid request format'}), 400
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)