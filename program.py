from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

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

@app.route("/student/<string:username>/<string:password>", methods=['GET'])
def get_student(id):
    student = db.session.get(Students, id)
    if not student:
        return jsonify(
            {
                "Login Sucess": False,
                "message": "Account not found"
            }
        ), 404
    return jsonify (
        {
            "Login Success": True,
            "data": student.to_dict()
        }
    ), 200

if __name__ == '__main__':
    app.run(debug=True)