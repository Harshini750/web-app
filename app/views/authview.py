import traceback
from datetime import timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime

from exceptions import FormValidationError
from models.user import User
from models.userhistory import UserHistory
from utils.password import Password

authview = Blueprint("authview", __name__)


@authview.route("/login")
def login_page():
    if current_user.is_authenticated:
        # Already logged-in
        return redirect(url_for("appview.index"))
    return render_template(
        "login-signup.html",
        title="Cardio Predict | Loign",
        page_header="Cardio Predict",
    )


@authview.route("/login", methods=["POST"])
def login_verify():
    try:
        email = request.form.get("email")
        passw = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user:
            raise FormValidationError("Incorrect username or password")

        if Password.verify_password(passw, user.password):
            login_user(user, remember=True, duration=timedelta(days=7))
            UserHistory.create(user=user, login_time=datetime.utcnow())
            return redirect(url_for("appview.index"))
        else:
            raise FormValidationError("Incorrect username or password")
    except FormValidationError as e:
        flash(str(e))
        return redirect(url_for("authview.login_page"))
    except:
        print(traceback.format_exc())
        flash("Something went wrong. Contact Admin.")
        return redirect(url_for("authview.login_page"))


@authview.route("/signup", methods=["POST"])
def signup():
    try:
        full_name = request.form.get("fullname")
        email = request.form.get("email")
        passw = request.form.get("password")
        passw_confirm = request.form.get("password_confirm")

        user = User.query.filter_by(email=email).first()
        if user:
            raise FormValidationError("This email is already registered. Please login.")

        if passw != passw_confirm:
            raise FormValidationError("Passwords do not match")

        user = User(
            name=full_name, email=email, password=Password.gen_hash(passw)
        ).save()
        login_user(user)
        UserHistory.create(user=user, login_time=datetime.utcnow())
        return redirect(url_for("appview.prediction"))
    except FormValidationError as e:
        flash(str(e))
        return redirect(url_for("authview.login_page"))
    except:
        print(traceback.format_exc())
        flash("Something went wrong. Contact Admin.")
        return redirect(url_for("authview.login_page"))


@authview.route("/logout")
@login_required
def logout():
    userhistory = (
        UserHistory.query.filter_by(user=current_user)
        .order_by(UserHistory.login_time.desc())
        .first()
    )
    if userhistory:
        userhistory.logout_time = datetime.utcnow()
        userhistory.save()
    logout_user()
    return redirect(url_for("appview.index"))
