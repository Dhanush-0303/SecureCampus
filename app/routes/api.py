from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.student import Student

api_bp = Blueprint('api', __name__)

@api_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200