from flask import Blueprint, render_template
from app.models.employee import Employee
from app.models.department import Department

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
@home_bp.route("/home")
def home():
    emp_count = Employee.query.count()
    dept_count = Department.query.count()
    return render_template("home.html", emp_count=emp_count, dept_count=dept_count)
