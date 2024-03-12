from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flask import request
from app import app
from .extensions import db
from app.forms import LoginForm, TicketForm, RegistrationForm, DeleteTicketForm, AmendTicketForm, AdminChangeStatusForm, AdminChangeNotesForm
from app.models import Ticket, User

def flash_error_messages(form_errors):
    for fieldName, errorMessages in form_errors.items():
        for err in errorMessages:
            flash(f"{fieldName}: {err}")

# Index route (User Dashboard)
@app.route('/')
@login_required  # Requires the user to be logged in
def index():
    user_tickets = current_user.tickets
    return render_template('index.html', user=current_user, tickets=user_tickets)

# Admin route (Admin Dashboard)
@app.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'warning')
        return redirect(url_for('dashboard'))

    admin_change_status_form = AdminChangeStatusForm(prefix="status")
    admin_change_notes_form = AdminChangeNotesForm(prefix="notes")

    if admin_change_status_form.save_changes.data and admin_change_status_form.validate_on_submit():
        ticket_id_to_change = admin_change_status_form.id.data
        status = admin_change_status_form.status.data
        
        ticket_to_amend = Ticket.query.get(ticket_id_to_change)
        if ticket_to_amend:
            ticket_to_amend.status = status
            db.session.commit()
    elif admin_change_status_form.save_changes.data:
        flash_error_messages(admin_change_status_form.errors)

    if admin_change_notes_form.save_notes.data and admin_change_notes_form.validate_on_submit():
        ticket_id_to_change = admin_change_notes_form.id.data
        notes = admin_change_notes_form.notes.data

        ticket_to_amend = Ticket.query.get(ticket_id_to_change)
        if ticket_to_amend:
            ticket_to_amend.notes = notes
            db.session.commit()
    elif admin_change_notes_form.save_notes.data:
        flash_error_messages(admin_change_notes_form.errors)
    
    all_tickets = Ticket.query.all()
    return render_template('admin.html', tickets=all_tickets, admin_change_status_form=admin_change_status_form, admin_change_notes_form=admin_change_notes_form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #print(user.password, form.password.data) - checked correct password for user
        if user and user.password == form.password.data:
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    else:
        print(form.errors)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user and add it to the database
        print("got form")
        user = User(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            is_admin=False,  # Assuming newly registered users are not admins
        )
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    else:
        flash_error_messages(form.errors)

    
    return render_template('register.html', form=form)

# Logout route
@app.route('/logout')
@login_required  # Requires the user to be logged in
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Ticket creation form
    create_ticket_form = TicketForm(prefix="create")

    # create_ticket_form.submit.data = True if create_ticket_form was submitted
    # amend_ticket_form.submit.data = True if amend_ticket_form was submitted

    # create_ticket_form.validate_on_submit() = True if create_ticket_form data is valid

    if create_ticket_form.submit_create.data and create_ticket_form.validate_on_submit():
        # Create a new ticket and add it to the database
        ticket = Ticket(title=create_ticket_form.title.data, description=create_ticket_form.description.data, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket created successfully.', 'success')
        return redirect(url_for('dashboard'))
    elif create_ticket_form.submit_create.data:
        flash_error_messages(create_ticket_form.errors)

    # Fetch all tickets for the current user
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
 
    amend_id = request.args.get('id') # 2
    amend_ticket = None
    if amend_id:
        amend_ticket = Ticket.query.get(amend_id)

    # Ticket amendment form
    amend_ticket_form = AmendTicketForm(obj=amend_ticket, prefix="amend")

    if amend_ticket_form.submit_amend.data and amend_ticket_form.validate_on_submit():
        ticket_id_to_amend = amend_ticket_form.id.data
        ticket_to_amend = Ticket.query.get(ticket_id_to_amend)
        if ticket_to_amend:
            # Update the ticket's title and description
            ticket_to_amend.title = amend_ticket_form.title.data
            ticket_to_amend.description = amend_ticket_form.description.data
            db.session.commit()
            flash('Ticket amended successfully.', 'success')
            return redirect(url_for('dashboard'))
    elif amend_ticket_form.submit_amend.data:
        flash_error_messages(amend_ticket_form.errors)
        
    delete_ticket_form =  DeleteTicketForm()

    # Ticket deletion
    if delete_ticket_form.validate_on_submit():
        ticket_id_to_delete = delete_ticket_form.id.data
        ticket_to_delete = Ticket.query.get(ticket_id_to_delete)

        if ticket_to_delete:
            # Delete the ticket from the database
            db.session.delete(ticket_to_delete)
            db.session.commit()
            flash('Ticket deleted successfully.', 'success')
            return redirect(url_for('dashboard'))
    else:
        flash_error_messages(delete_ticket_form.errors)

    return render_template('index.html', title='Dashboard', create_ticket_form=create_ticket_form,
                           amend_ticket_form=amend_ticket_form, tickets=tickets, delete_ticket_form=delete_ticket_form, amend_ticket=amend_ticket)
