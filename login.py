from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
import re
import hashlib
import hmac
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_default_key')

db = SQLAlchemy(app)

class Students(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profileImagePath = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.firstName,
            "last_name": self.lastName,
            "gender": self.gender,
            "username": self.username,
            "hashPassword": self.password,
            "image_path": self.image_path if self.profileImagePath else "default.png"
        }

def is_valid_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_.-]{3,50}$', username))

def is_valid_password(password):
    return len(password) >= 6

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/student/login", methods=['POST'])
def login_student():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not is_valid_username(username):
        return jsonify({
            "Login Success": False,
            "message": "Invalid username format"
        }), 400

    if not password or not is_valid_password(password):
        return jsonify({
            "Login Success": False,
            "message": "Password must be at least 6 characters long"
        }), 400

    student = Students.query.filter_by(username=username).first()
    
    if not student:
        return jsonify({
            "Login Success": False,
            "message": "Username not found"
        }), 404
    
    if not hmac.compare_digest(student.password, hash_password(password)):
        return jsonify({
            "Login Success": False,
            "message": "Incorrect password"
        }), 401
    
    session['user_id'] = student.id
    session['username'] = student.username
    
    return jsonify({
        "Login Success": True,
        "message": "Login successful",
        "data": student.to_dict()
    }), 200

@app.route("/student/logout", methods=['POST'])
def logout_student():
    session.pop('user_id', None)
    session.pop('username', None)
    return jsonify({
        "Logout Success": True,
        "message": "Successfully logged out"
    }), 200

@app.route("/student/status", methods=['GET'])
def session_status():
    if 'user_id' in session:
        return jsonify({
            "Logged In": True,
            "user_id": session['user_id'],
            "username": session['username']
        }), 200
    return jsonify({
        "Logged In": False,
        "message": "No active session"
    }), 401

if __name__ == '__main__':
    app.run(debug=True)
