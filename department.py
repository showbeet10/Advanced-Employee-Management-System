from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app.models import db
from app.models.department import Department

department_bp = Blueprint("department", __name__)

@department_bp.route("/department")
def department_list():
    departments = Department.query.order_by(Department.name.asc()).all()
    return render_template("department.html", departments=departments)

@department_bp.route("/department/add", methods=["GET", "POST"])
def department_add():
    if request.method == "POST":
        try:
            dept = Department(
                name=request.form["name"].strip(),
                description=request.form.get("description", "").strip()
            )
            db.session.add(dept)
            db.session.commit()
            flash("Department added successfully.", "success")
            return redirect(url_for("department.department_list"))
        except IntegrityError:
            db.session.rollback()
            flash("A department with this name already exists.", "danger")
        except Exception as e:
            db.session.rollback()
            flash("Error adding department.", "danger")
    return render_template("add_department.html")

@department_bp.route("/department/update/<int:id>", methods=["GET", "POST"])
def department_update(id):
    dept = Department.query.get_or_404(id)
    if request.method == "POST":
        try:
            dept.name = request.form["name"].strip()
            dept.description = request.form.get("description", "").strip()
            db.session.commit()
            flash("Department updated successfully.", "success")
            return redirect(url_for("department.department_list"))
        except IntegrityError:
            db.session.rollback()
            flash("A department with this name already exists.", "danger")
    return render_template("update_department.html", department=dept)

@department_bp.route("/department/delete/<int:id>")
def department_delete(id):
    dept = Department.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    flash("Department deleted successfully.", "success")
    return redirect(url_for("department.department_list"))