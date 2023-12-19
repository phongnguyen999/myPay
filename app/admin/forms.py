# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
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

class EmployeeForm(FlaskForm):
    """
    Form for admin to add new employee
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    rate = QuerySelectField(query_factory=lambda: Rate.query.all(),
                                  get_label="name")
    submit = SubmitField('Add')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')