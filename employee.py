from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import asc, desc, or_
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.models.employee import Employee

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/employee/<int:id>/<string:name>")
def searchByNameId(id, name):
    return f"ID : {id} Name : {name}"


@employee_bp.route("/employee")
def displaySpecific():
    department = request.args.get("department")
    page = request.args.get("page")
    return f"Department : {department} Page : {page}"


@employee_bp.route("/employeeDepartment")
def gotodept():
    return redirect(url_for("department.departmentHome"))


@employee_bp.route("/employee/register")
def register_employee():
    return render_template("add_employee.html")


@employee_bp.route("/employee/list")
def employee_list():
    """Employee list with combined search, filters, sorting and pagination."""
    search = request.args.get("search", "", type=str).strip()
    department = request.args.get("department", "", type=str).strip()
    min_salary = request.args.get("min_salary", "", type=str).strip()
    max_salary = request.args.get("max_salary", "", type=str).strip()
    sort_by = request.args.get("sort_by", "name", type=str)
    sort_order = request.args.get("sort_order", "asc", type=str).lower()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if per_page not in (5, 10):
        per_page = 5

    query = Employee.query

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Employee.name.ilike(pattern),
                Employee.email.ilike(pattern),
                Employee.department.ilike(pattern),
            )
        )

    if department:
        query = query.filter(Employee.department == department)

    try:
        if min_salary:
            query = query.filter(Employee.salary >= float(min_salary))
        if max_salary:
            query = query.filter(Employee.salary <= float(max_salary))
    except ValueError:
        flash("Salary filters must contain valid numbers.", "danger")

    sortable_columns = {
        "name": Employee.name,
        "email": Employee.email,
        "department": Employee.department,
        "salary": Employee.salary,
    }
    sort_column = sortable_columns.get(sort_by, Employee.name)
    order_function = desc if sort_order == "desc" else asc
    query = query.order_by(order_function(sort_column), Employee.id.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    departments = [
        row[0]
        for row in db.session.query(Employee.department)
        .distinct()
        .order_by(Employee.department.asc())
        .all()
    ]

    return render_template(
        "employee.html",
        employees=pagination.items,
        pagination=pagination,
        departments=departments,
        search=search,
        selected_department=department,
        min_salary=min_salary,
        max_salary=max_salary,
        sort_by=sort_by,
        sort_order=sort_order,
        per_page=per_page,
    )


@employee_bp.route("/employee/add", methods=["POST", "GET"])
def employeeAdd():
    if request.method == "POST":
        try:
            employee = Employee(
                name=request.form["name"].strip(),
                email=request.form["email"].strip(),
                password=request.form["password"],
                salary=float(request.form["salary"]),
                department=request.form["department"].strip(),
            )
            db.session.add(employee)
            db.session.commit()
            flash("Employee added successfully.", "success")
            return redirect(url_for("employee.employee_list"))
        except (ValueError, KeyError):
            db.session.rollback()
            flash("Please enter valid employee details.", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("An employee with this email already exists.", "danger")

    return render_template("add_employee.html")


@employee_bp.route("/employee/employeeDetail/<int:id>", methods=["GET"])
def employeeDetail(id):
    employee = Employee.query.get_or_404(id)
    return render_template("employee_detail.html", employee=employee)


@employee_bp.route("/employee/employeeUpdate/<int:id>", methods=["POST", "GET"])
def employeeUpdate(id):
    employee = Employee.query.get_or_404(id)

    if request.method == "POST":
        try:
            employee.name = request.form["name"].strip()
            employee.email = request.form["email"].strip()
            employee.password = request.form["password"]
            employee.salary = float(request.form["salary"])
            employee.department = request.form["department"].strip()
            db.session.commit()
            flash("Employee updated successfully.", "success")
            return redirect(url_for("employee.employee_list"))
        except (ValueError, KeyError):
            db.session.rollback()
            flash("Please enter valid employee details.", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("Another employee is already using this email.", "danger")

    return render_template("update_employee.html", employee=employee)


@employee_bp.route("/employee/employeeDelete/<int:id>")
def employeeDelete(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee deleted successfully.", "success")
    return redirect(url_for("employee.employee_list"))
