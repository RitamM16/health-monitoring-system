from flask import Flask, request, jsonify
from Data.Models import Endpoint
from Data.Database import initSQLAlchemy
from Data.Celery import createHealthCheck, removeHealthCheck

app = Flask(__name__)

db = initSQLAlchemy(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_endpoint = Endpoint(
        owner=data['owner'], # type: ignore
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
def get_all_endpoints():
    endpoints = Endpoint.query.where(Endpoint.is_deleted == 0).all()
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
def get_endpoint(endpoint_id):
    endpoint = Endpoint.query.where(Endpoint.is_deleted == 0, Endpoint.id == endpoint_id).first()
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
def delete_endpoint(endpoint_id):
    endpoint = Endpoint.query.where(Endpoint.is_deleted == 0, Endpoint.id == endpoint_id).first()
    if not endpoint:
        return jsonify({"message": "Endpoint not found"}), 404
    
    Endpoint.query.where(Endpoint.is_deleted == 0, Endpoint.id == endpoint_id).update({Endpoint.is_deleted: 1})
    
    db.session.commit()
    
    removeHealthCheck(str(endpoint_id))
    
    return jsonify({"message": "Endpoint deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)