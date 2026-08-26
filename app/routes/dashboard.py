from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required  # Restricts page to logged-in users
from app import db                       # Your SQLAlchemy database instance
from app.models.student import Student   # Your Student database model

dashboard_bp = Blueprint('dashboard', __name__)

# 1. Main Dashboard (Displays dynamic metrics)
@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    total_students = Student.query.count()
    return render_template('dashboard/index.html', total_students=total_students)

# 2. Student Directory (Fetches students from database)
@dashboard_bp.route('/students')

def students():
    student_list = Student.query.all()
    return render_template('dashboard/students.html', students=student_list)

# 3. Add New Student (Processes the form post request)
@dashboard_bp.route('/students/add', methods=['POST'])

def add_student():
    name = request.form.get('name')
    email = request.form.get('email')
    department = request.form.get('department')

    new_student = Student(name=name, email=email, department=department)
    db.session.add(new_student)
    db.session.commit()

    flash('Student added successfully!', 'success')
    return redirect(url_for('dashboard.students'))

# 4. Settings Page
@dashboard_bp.route('/settings')

def settings():
    return render_template('dashboard/settings.html')