import traceback
from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from controllers.predictioncontroller import PredictionController
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
        "heartrisk.html",
        title="Cardio Predict | Prediction",
        page_header="Cardio Predict",
    )


@appview.route("/predict", methods=["POST"])
def predict():
    try:
        form_data = request.form.to_dict()
        controller = PredictionController(form_data)
        result = controller.predict()
        
        # Save to DB
        controller.save_to_db(current_user)    

        return render_template(
            "heartrisk.html",
            title="Cardio Predict | Prediction",
            page_header="Cardio Predict",
            result=result
        )

    except FormValidationError as e:
        flash(str(e))
        return redirect(url_for("appview.prediction"))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        flash("Something went wrong. Could not make prediction.")
        return redirect(url_for("appview.prediction"))
