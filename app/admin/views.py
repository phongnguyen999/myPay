# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import SaleForm, RateForm, EmployeeAssignForm, EmployeeForm
from .. import db
from ..models import Sale, Rate, Employee

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/sales', methods=['GET', 'POST'])
@login_required
def list_sales():
    """
    List all sales
    """
    check_admin()

    sales = Sale.query.all()

    return render_template('admin/sales/sales.html',
                           sales=sales, title="Sales")

@admin.route('/sales/add', methods=['GET', 'POST'])
@login_required
def add_sale():
    """
    Add a sale to the database
    """
    check_admin()

    add_sale = True

    form = SaleForm()
    if form.validate_on_submit():
        sale = Sale(employee=form.employee.data, date = form.date.data, is_approved = form.is_approved.data,
                                amount=form.amount.data, )
        try:
            # add department to the database
            db.session.add(sale)
            db.session.commit()
            flash('You have successfully added a new sale.')
        except:
            # in case department name already exists
            flash('Error: sale already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_sales'))

    # load department template
    return render_template('admin/sales/sale.html', action="Add",
                           add_sale=add_sale, form=form,
                           title="Add Sale")

@admin.route('/sales/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sale(id):
    """
    Edit a sale
    """
    check_admin()

    add_sale = False

    sale = Sale.query.get_or_404(id)
    form = SaleForm(obj=sale)
    if form.validate_on_submit():
        sale.employee = form.employee.data
        sale.amount = form.amount.data
        sale.date = form.date.data
        sale.is_approved = form.is_approved.data
        db.session.commit()
        flash('You have successfully edited the sale.')

        return redirect(url_for('admin.list_sales'))

    return render_template('admin/sales/sale.html', action="Edit",
                           add_sale=add_sale, form=form,
                           sale=sale, title="Edit Sale")

@admin.route('/sales/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_sale(id):
    """
    Delete a sale record from the database
    """
    check_admin()

    sale = Sale.query.get_or_404(id)
    db.session.delete(sale)
    db.session.commit()
    flash('You have successfully deleted the record.')

    return redirect(url_for('admin.list_sales'))

    return render_template(title="Delete Record")


@admin.route('/rates')
@login_required
def list_rates():
    check_admin()
    """
    List all rates
    """
    rates = Rate.query.all()
    return render_template('admin/rates/rates.html',
                           rates=rates, title='Rates')

@admin.route('/rates/add', methods=['GET', 'POST'])
@login_required
def add_rate():
    """
    Add a rate to the database
    """
    check_admin()

    add_rate = True

    form = RateForm()
    if form.validate_on_submit():
        rate = Rate(name=form.name.data,
                    description=form.description.data)

        try:
            db.session.add(rate)
            db.session.commit()
            flash('You have successfully added a new rate.')
        except:
            flash('Error: rate already exists.')

        return redirect(url_for('admin.list_rates'))

    return render_template('admin/rates/rate.html', add_rate=add_rate,
                           form=form, title='Add Rate')

@admin.route('/rates/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_rate(id):
    """
    Edit a rate
    """
    check_admin()

    add_rate = False

    rate = Rate.query.get_or_404(id)
    form = RateForm(obj=rate)
    if form.validate_on_submit():
        rate.name = form.name.data
        rate.description = form.description.data
        db.session.add(rate)
        db.session.commit()
        flash('You have successfully edited the rate.')

        return redirect(url_for('admin.list_rates'))

    form.description.data = rate.description
    form.name.data = rate.name
    return render_template('admin/rates/rate.html', add_rate=add_rate,
                           form=form, title="Edit Rate")

@admin.route('/rates/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_rate(id):
    """
    Delete a rate from the database
    """
    check_admin()

    rate = Rate.query.get_or_404(id)
    db.session.delete(rate)
    db.session.commit()
    flash('You have successfully deleted the rate.')

    return redirect(url_for('admin.list_rates'))

    return render_template(title="Delete Rate")


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    employees = sorted(employees, key=lambda x: not x.is_admin)

    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')

@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a rate to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a rate
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.rate = form.rate.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a rate.')

        # redirect to the employees page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')


@admin.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    """
    Add an employee to the database
    """
    check_admin()

    add_employee = True

    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            rate = form.rate.data,
                            password=form.password.data)
        try:
            db.session.add(employee)
            db.session.commit()
            flash('You have successfully added a new employee.')
        except:
            flash('Error: Employee already exists.')

        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html', add_employee=add_employee,
                           form=form, title='Add Employee')