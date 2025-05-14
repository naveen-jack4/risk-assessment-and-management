
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from cryptography.fernet import Fernet

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret'

db = SQLAlchemy(app)
jwt = JWTManager(app)

cipher = Fernet(Fernet.generate_key())  # Store this securely

class PatientData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encrypted_data = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

@app.route('/data', methods=['POST'])
@jwt_required()
def store_data():
    user_id = get_jwt_identity()
    plain_data = request.json['data'].encode()
    encrypted = cipher.encrypt(plain_data)
    db.session.add(PatientData(encrypted_data=encrypted, user_id=user_id))
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_panel():
    if get_jwt_identity() != 'admin':
        return jsonify({'error': 'unauthorized'}), 403
    return jsonify({'admin_data': 'secure content'})
