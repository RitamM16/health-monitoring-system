from flask import Flask, request, jsonify
from flask_login import LoginManager
from Data.Models import Endpoint, User
from Data.Database import initSQLAlchemy
from Data.Celery import createHealthCheck, removeHealthCheck
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

db = initSQLAlchemy(app)

# This is not recommended for production
app.secret_key = "super secret key"

login_manager = LoginManager(app)
login_manager.login_view = 'login' # type: ignore

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.json
    if User.query.filter_by(email=data['email']).first() is not None: # type: ignore
        return jsonify({"message": "Email already registered"}), 400
    
    new_user = User(
        email=data['email'], # type: ignore
        name=data['name'] # type: ignore
    ) # type: ignore
    new_user.set_password(data['password']) # type: ignore
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered"}), 201

@app.route('/user/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first() # type: ignore
    if user is None or not user.check_password(data['password']): # type: ignore
        return jsonify({"message": "Invalid email or password"}), 401
    
    login_user(user)
    return jsonify({"message": "Logged in successfully"}), 200

@app.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/endpoints/register', methods=['POST'])
@login_required
def register():
    data = request.json
    new_endpoint = Endpoint(
        owner=current_user.id, # type: ignore
        url=data['url'], # type: ignore
        frequency=data['frequency'], # type: ignore
        method=data['method'], # type: ignore
        headers=data['headers'], # type: ignore
        success_criteria_status_code=data['success_criteria_status_code'], # type: ignore
        success_criteria_response_time=data['success_criteria_response_time'], # type: ignore
        unhealthy_threshold_count=data['unhealthy_threshold_count'] # type: ignore
    ) # type: ignore
    
    db.session.add(new_endpoint)
    db.session.commit()
    
    createHealthCheck(str(new_endpoint.id), new_endpoint.frequency)
    
    return jsonify({"message": "Endpoint registered"}), 201

@app.route('/endpoints', methods=['GET'])
@login_required
def get_all_endpoints():
    endpoints = Endpoint.query.where(Endpoint.is_deleted == 0, Endpoint.owner == current_user.id).all()
    result = [
        {
            "id": endpoint.id,
            "owner": endpoint.owner,
            "url": endpoint.url,
            "frequency": endpoint.frequency,
            "method": endpoint.method,
            "headers": endpoint.headers,
            "success_criteria_status_code": endpoint.success_criteria_status_code,
            "success_criteria_response_time": endpoint.success_criteria_response_time,
            "unhealthy_threshold_count": endpoint.unhealthy_threshold_count
        }
        for endpoint in endpoints
    ]
    return jsonify(result), 200

@app.route('/endpoints/<int:endpoint_id>', methods=['GET'])
@login_required
def get_endpoint(endpoint_id):
    endpoint = Endpoint.query.where(Endpoint.is_deleted == 0, Endpoint.id == endpoint_id, Endpoint.owner == current_user.id).first()
    if not endpoint:
        return jsonify({"message": "Endpoint not found"}), 404
    
    result = {
        "id": endpoint.id,
        "owner": endpoint.owner,
        "url": endpoint.url,
        "frequency": endpoint.frequency,
        "method": endpoint.method,
        "headers": endpoint.headers,
        "success_criteria_status_code": endpoint.success_criteria_status_code,
        "success_criteria_response_time": endpoint.success_criteria_response_time,
        "unhealthy_threshold_count": endpoint.unhealthy_threshold_count
    }
    return jsonify(result), 200

@app.route('/endpoints/<int:endpoint_id>', methods=['DELETE'])
@login_required
def delete_endpoint(endpoint_id):
    endpoint = Endpoint.query.where(Endpoint.is_deleted == 0, Endpoint.id == endpoint_id, Endpoint.owner == current_user.id).first()
    if not endpoint:
        return jsonify({"message": "Endpoint not found"}), 404
    
    Endpoint.query.where(Endpoint.is_deleted == 0, Endpoint.id == endpoint_id, Endpoint.owner == current_user.id).update({Endpoint.is_deleted: 1})
    
    db.session.commit()
    
    removeHealthCheck(str(endpoint_id))
    
    return jsonify({"message": "Endpoint deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)