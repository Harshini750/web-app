import traceback
from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from utils.prediction import Prediction
from exceptions import FormValidationError

appview = Blueprint("appview", __name__)


@appview.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("appview.prediction"))
    else:
        return redirect(url_for("authview.login_page"))


@appview.route("/predict")
@login_required
def prediction():
    return render_template(
        "heartrisk.html", title="Cardio Predict | Loign", page_header="Cardio Predict"
    )


@appview.route("/predict", methods=["POST"])
def predict():
    try:
        if request.method == "POST":
            to_predict_list = request.form.to_dict()
            to_predict_list = list(to_predict_list.values())
            to_predict_list = list(map(float, to_predict_list))

            if len(to_predict_list) == 11:
                result = Prediction.value_predictor(to_predict_list, 11)

            else:
                print(request.form.to_dict())
                raise FormValidationError("Incorrect number of fields received")

        return render_template("heartrisk.html", result=result)

    except FormValidationError as e:
        flash(str(e))
        return redirect(url_for("appview.prediction"))
    except:
        print(traceback.format_exc())
        flash("Something went wrong. Could not make prediction.")
        return redirect(url_for("appview.prediction"))
