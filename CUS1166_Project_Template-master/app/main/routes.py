from flask import render_template, redirect, url_for
from app.main import bp
from app import db
from app.main.forms import TaskForm, AppointmentForm
from app.models import Task, Appointment


# Main route of the applicaitons.
from sqlalchemy import desc, func


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("main/index.html")


#
#  Route for viewing and adding new tasks.
@bp.route('/todolist', methods=['GET', 'POST'])
def todolist():
    form = TaskForm()

    if form.validate_on_submit():
        # Get the data from the form, and add it to the database.
        new_task = Task()
        new_task.task_desc = form.task_desc.data
        new_task.task_status = form.task_status_completed.data

        db.session.add(new_task)
        db.session.commit()

        # Redirect to this handler - but without form submitted - gets a clear form.
        return redirect(url_for('main.todolist'))

    todo_list = db.session.query(Task).all()

    return render_template("main/todolist.html", todo_list=todo_list, form=form)


#
# Route for removing a task
@bp.route('/todolist/remove/<int:task_id>', methods=['GET', 'POST'])
def remove_task(task_id):
    # Query database, remove items
    Task.query.filter(Task.task_id == task_id).delete()
    db.session.commit()

    return redirect(url_for('main.todolist'))


#
# Route for editing a task

@bp.route('/todolist/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    form = TaskForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        # Get the data from the form, and add it to the database.

        current_task = Task.query.filter_by(task_id=task_id).first_or_404()
        current_task.task_desc = form.task_desc.data
        current_task.task_status = form.task_status_completed.data

        db.session.add(current_task)
        db.session.commit()
        # After editing, redirect to the view page.
        return redirect(url_for('main.todolist'))

    # get task for the database.
    current_task = Task.query.filter_by(task_id=task_id).first_or_404()

    # update the form model in order to populate the html form.
    form.task_desc.data = current_task.task_desc
    form.task_status_completed.data = current_task.task_status

    return render_template("main/todolist_edit_view.html", form=form, task_id=task_id)


@bp.route('/ScheduleAppointment', methods=['GET', 'POST'])
def Schedule():
    form = AppointmentForm()
    if form.validate_on_submit():
        new_appointment = Appointment()

        new_appointment.customer_name = form.customer_name.data
        new_appointment.appointment_title = form.appointment_title.data
        new_appointment.appointment_date = form.appointment_date.data
        new_appointment.appointment_time = form.start_time.data
        new_appointment.appointment_duration = form.duration_of_appointment.data
        new_appointment.appointment_location = form.location.data
        new_appointment.notes = form.notes.data
        new_appointment.appointment_status = form.appointment_status_completed.data

        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('main.view_schedule'))
    return render_template('main/schedule_appointment.html', title='Schedule an appointment', form=form)


@bp.route('/Schedule/edit/<int:appointment_id>', methods=['GET', 'POST'])
def Update_Schedule(appointment_id):
    form = AppointmentForm()
    if form.validate_on_submit():
        current_appointment = Appointment.query.filter_by(appointment_id=appointment_id).first_or_404()
        current_appointment.customer_name = form.customer_name.data
        current_appointment.appointment_title = form.appointment_title.data
        current_appointment.appointment_date = form.appointment_date.data
        current_appointment.appointment_time = form.start_time.data
        current_appointment.appointment_duration = form.duration_of_appointment.data
        current_appointment.appointment_location = form.location.data
        current_appointment.appointment_status = form.appointment_status_completed.data
        current_appointment.notes = form.notes.data

        db.session.add(current_appointment)
        db.session.commit()

        return redirect(url_for('main.view_schedule'))

    current_appointment = Appointment.query.filter_by(appointment_id=appointment_id).first_or_404()

    form.customer_name.data = current_appointment.customer_name
    form.appointment_title.data = current_appointment.appointment_title
    form.appointment_date.data = current_appointment.appointment_date
    form.start_time.data = current_appointment.appointment_time
    form.duration_of_appointment.data = current_appointment.appointment_duration
    form.location.data = current_appointment.appointment_location
    form.appointment_status_completed.data = current_appointment.appointment_status
    form.notes.data = current_appointment.notes

    return render_template('main/schedule_appointment.html', title='Schedule an appointment', form=form)


@bp.route('/Schedule/remove/<int:appointment_id>', methods=['GET', 'POST'])
def remove_schedule(appointment_id):
    # Query database, remove items
    Appointment.query.filter(Appointment.appointment_id == appointment_id).delete()
    db.session.commit()

    return redirect(url_for('main.view_schedule'))


@bp.route('/ViewAppointments', methods=['GET', 'POST'])
def view_schedule():
    schedule = db.session.query(Appointment).order_by(func.DATE(Appointment.appointment_date)).all()

    return render_template('main/display_schedules.html', schedule=schedule)


@bp.route('/view_appointment_info/<int:appointment_id>', methods=['GET', 'POST'])
def view_apppointment_info(appointment_id):
    current_appointment = Appointment.query.filter_by(appointment_id=appointment_id).first_or_404()
    return render_template('main/display_appointment_info.html', current_appointment=current_appointment)