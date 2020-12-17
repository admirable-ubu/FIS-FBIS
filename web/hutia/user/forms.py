from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask import flash
from flask_login import current_user
from hutia.model import User


class LoginForm(FlaskForm):
    """Formulario para el login de los usuarios.
    
    Arguments:
        FlaskForm {FlaskForm} -- Flask wtform.
    """
    identity = StringField("Identificador", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")


class ChangePassForm(FlaskForm):
    """Formulario para cambiar la contraseña.
    
    Arguments:
        FlaskForm {FlaskForm} -- Flask wtform.
    """
    password_old = PasswordField("Contraseña anterior", validators=[DataRequired()])
    password_new = PasswordField("Contraseña nueva", validators=[DataRequired()])
    password_new_re = PasswordField("Repite la contraseña nueva", validators=[DataRequired(), EqualTo('password_new')])
    submit = SubmitField("Cambiar la contraseña")