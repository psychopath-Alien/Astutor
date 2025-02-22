from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
@app.route("/validate", methods=['POST'])
def validate():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        student = db.session.query(Students).filter_by(username=username).first()

        if student and check_password_hash(student.password, password):
            return jsonify({"Validation Success": True, "data": student.to_dict()}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {str(err)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)