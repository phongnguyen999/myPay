# app/home/views.py

from flask import abort, render_template
from flask_login import login_required, current_user
from ..models import Sale, Rate, Employee

from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    # prevent admins from accessing the page
    if current_user.is_admin:
        abort(403)

    employee = Employee.query.get_or_404(current_user.id)

    return render_template('home/dashboard.html', employee=employee, title="Dashboard")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")