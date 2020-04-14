from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class DataForm(FlaskForm):
    population = IntegerField('Population', validators=[DataRequired()])
    time_to_elapse = IntegerField(
        'Time To Elapse', validators=[DataRequired()])
    reported_cases = IntegerField(
        'Reported Cases', validators=[DataRequired()])
    hospital_beds = IntegerField(
        'Total Hospital Beds', validators=[DataRequired()])
    period_type = SelectField('Period Type', choices=[(
        'days', 'Days'), ('weeks', 'weeks'), ('months', 'Months')])
    submit = SubmitField('Estimate')
