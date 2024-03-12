from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

# LoginForm for user login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

# TicketForm for creating new tickets
class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit_create = SubmitField('Submit Ticket')

# TicketForm for amending new tickets
class AmendTicketForm(FlaskForm):
    id = StringField('Ticket ID', validators=[DataRequired(), Length(max=100)])
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit_amend = SubmitField('Amend Ticket')

#TicketForm for deleting tickets
class DeleteTicketForm(FlaskForm):
    id = StringField('ticket id', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Delete Ticket')

#RegistrationForm with the appropriate parameters
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use. Please choose a different one.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email address is already registered. Please use a different one.')

#Forms for the admin dashboard to change status and notes
class AdminChangeStatusForm(FlaskForm):
    id = StringField('ticket id', validators=[DataRequired(), Length(max=100)])
    status = SelectField("Ticket Status", choices=[("WAITING", "Waiting"), ("IN_PROGRESS", "In Progress"), ("DONE", "Done")])
    save_changes = SubmitField('Save Changes')


class AdminChangeNotesForm(FlaskForm):
    id = StringField('ticket id', validators=[DataRequired(), Length(max=100)])
    notes = StringField("Notes", validators=[Length(max=500)])
    save_notes = SubmitField('Save Notes')
    
    # submit = SubmitField('Save Notes')/
