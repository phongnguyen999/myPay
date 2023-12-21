from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from ..models import Sale, Rate, Employee
from .. import db
from . import mypay
from .forms import SaleForm


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if current_user.is_admin:
        abort(403)

@mypay.route('/mypay')
@login_required
def sales():
    """
    Render the dashboard template on the /dashboard route
    """
    # prevent admins from accessing the page
    check_admin()

    employee = Employee.query.get_or_404(current_user.id)
    sales = employee.sales.all()

    return render_template('mypay/mypays.html', sales=sales, employee=employee, title="Earnings")

@mypay.route('/mypay/add', methods=['GET', 'POST'])
@login_required
def add_sale():
    """
    Add a sale to the database
    """
    check_admin()

    add_sale = True
    employee = Employee.query.get_or_404(current_user.id)

    form = SaleForm()
    if form.validate_on_submit():
        sale = Sale(employee=employee, date = form.date.data,
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
        return redirect(url_for('mypay.sales'))
    return render_template('mypay/mypay.html', action="Add",
                           add_sale=add_sale, form=form,
                           title="Add Sale")

@mypay.route('/mypay/edit/<int:id>', methods=['GET', 'POST'])
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
        sale.amount = form.amount.data
        sale.date = form.date.data
        db.session.commit()
        flash('You have successfully edited the sale.')

        return redirect(url_for('mypay.sales'))

    return render_template('mypay/mypay.html', action="Edit",
                           add_sale=add_sale, form=form,
                           sale=sale, title="Edit Sale")

@mypay.route('/mypay/delete/<int:id>', methods=['GET', 'POST'])
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

    return redirect(url_for('mypay.sales'))

    return render_template(title="Delete Record")
