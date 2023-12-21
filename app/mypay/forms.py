from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DateTimeField
from datetime import date
from wtforms.validators import DataRequired

class SaleForm(FlaskForm):
    """
    Form for admin to add or edit a sale
    """
    amount = IntegerField('Amount', validators=[DataRequired()])
    date = DateTimeField("Today", format="%Y-%m-%d", default=date.today(),validators=[DataRequired()])
    submit = SubmitField('Submit')