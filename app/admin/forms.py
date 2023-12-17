# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField, BooleanField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from datetime import date
from ..models import Employee, Rate


class SaleForm(FlaskForm):
    """
    Form for admin to add or edit a sale
    """
    employee = QuerySelectField(query_factory=lambda: Employee.query.all(),
                                  get_label="username")
    amount = IntegerField('Amount', validators=[DataRequired()])
    date = DateTimeField("Today", format="%Y-%m-%d", default=date.today(),validators=[DataRequired()])
    is_approved = BooleanField('Approve',default='checked')
    submit = SubmitField('Submit')

class RateForm(FlaskForm):
    """
    Form for admin to add or edit a rate
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign rates to employees
    """
    rate = QuerySelectField(query_factory=lambda: Rate.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')