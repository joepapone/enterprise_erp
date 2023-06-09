from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError, EqualTo
from .models import User, Role


# Get roles to populate select field
def get_roles():
    list = [(row.role_id, row.role_name) for row in Role.query.all()]

    return list


# Validate for length
def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length


# User form attributes
class UserForm(FlaskForm):  
    user_name = fields.StringField(label='Name', validators=[length(min=3, max=50)], description="User name",
        render_kw={'class': 'field-data', 'placeholder': 'Name..'})
    role_id = fields.SelectField(label='Role', choices=get_roles ,validators=[InputRequired()], description="User role",
        render_kw={'class': 'field-data', 'autofocus': ""})
    email = fields.StringField(label='Email', validators=[length(min=3, max=120), Email()], description="User email",
        render_kw={'class': 'field-data', 'placeholder': 'Email..'})
    password = fields.PasswordField(label='Password', validators=[length(min=3, max=50)], description="User password",
        render_kw={'class': 'field-data', 'placeholder': 'Password..'})

    def validate_email(form, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A user with that email already exists")


# Change password form attributes
class ChangePasswordForm(FlaskForm):
    password = fields.PasswordField(label='Password', validators=[length(min=3, max=50), EqualTo('confirm', message='Passwords must match')], description="New password",
    render_kw={'class': 'field-data', 'placeholder': 'New password..'})
    confirm = fields.PasswordField(label='Password', validators=[length(min=3, max=50), EqualTo('confirm', message='Passwords must match')], description="Confirm password",
    render_kw={'class': 'field-data', 'placeholder': 'Confirm password..'})
        