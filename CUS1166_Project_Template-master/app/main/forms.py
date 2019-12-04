# import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField, TimeField
from wtforms.validators import ValidationError, DataRequired, Length


class TaskForm(FlaskForm):
    task_desc = StringField('task_desc', validators=[DataRequired()])
    task_status_completed = SelectField('Status', choices=[('todo', 'Todo'), ('doing', 'Doing'), ('done', 'Done')])
    submit = SubmitField('submit')


class AppointmentForm(FlaskForm):
    customer_name = StringField('Customers name', validators=[DataRequired()])
    appointment_title = StringField('Appointment Name', validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    duration_of_appointment = SelectField('Duration', choices=[('15 mins', '15 mins'), ('30 mins', '30 mins'),
                                                               ('45 mins', '45 mins'), ('1 hour', '1 hour'),
                                                               ('1.25 hours', '1.25 hour '), ('1.5 hours', '1.5 hour '),
                                                               ('1.75 hours', '1.75 hour '), ('2 hours', '2 hour ') ],
                                          validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    notes = StringField('Additional Notes')
    appointment_status_completed = SelectField('Status', choices=[('todo', 'Todo'), ('doing', 'Doing'), ('done', 'Done')])
    submit = SubmitField('Submit')
