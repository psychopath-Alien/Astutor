from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # added to store data
app.config['SECRET_KEY'] = 'your_secret_key_here'

Session(app)
db = SQLAlchemy(app)

class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "username": self.username,
            "password": self.password
        }

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    student = Students.query.filter_by(username=username, password=password).first()
    if not student:
        return jsonify({"Login Success": False, "message": "Account not found"}), 404
    
    session['student_id'] = student.id  # storing data of student
    return jsonify({"Login Success": True, "data": student.to_dict()}), 200

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('student_id', None)  # removing stored data of student
    return jsonify({"Logout Success": True, "message": "Logged out successfully"}), 200

@app.route("/student", methods=['GET'])
def get_student():
    if 'student_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    
    student = Students.query.get(session['student_id'])
    if not student:
        return jsonify({"message": "Student not found"}), 404
    
    return jsonify({"data": student.to_dict()}), 200

if __name__ == '__main__':
    app.run(debug=True)