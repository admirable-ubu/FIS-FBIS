from flask import render_template, Blueprint, redirect, url_for, request, flash, make_response
from hutia.user.forms import LoginForm, ChangePassForm
from flask_login import login_user, current_user, login_required
import variables as v
from hutia.model import User
import datetime


user = Blueprint("user", __name__)


@user.route("/", methods=["GET", "POST"])
def login():
    print(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(identity_name=form.identity.data).first()
            if user is not None and user.check_password(form.password.data):
                #login_user(user)
                response = make_response(redirect(url_for('core.index')))
                expire_date = datetime.datetime.now()
                expire_date = expire_date + datetime.timedelta(days=365000)
                response.set_cookie("token", user.token, expires=expire_date)
                return response
            else:
                flash("Error de credenciales", "danger")

    return render_template("login.html.j2", title="Hutia", form=form)


@v.login_manager.request_loader
def load_user_from_request(request):
    token = request.cookies.get('token')
    user = User.query.filter_by(token=token).first()
    return user

@user.route("/change_password", methods=["GET", "POST"])
def change_pass():
    print(current_user)
    form = ChangePassForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = current_user
            if user is not None and user.check_password(form.password_old.data):
                #login_user(user)
                response = make_response(redirect(url_for('core.index')))
                user.set_password(form.password_new.data)
                return response
            else:
                flash("Error de credenciales", "danger")
        else:
            flash("Las contraseñas no coinciden", "warning")
    return render_template("change_pass.html.j2", title="Hutia", form=form)

@user.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect(url_for('core.index')))
    response.set_cookie("token", "", expires=0)
    return response