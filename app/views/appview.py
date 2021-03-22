import traceback
from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from controllers.predictioncontroller import PredictionController
from exceptions import FormValidationError
from models.userhistory import UserHistory
from models.medicalrecord import MedicalRecord

appview = Blueprint("appview", __name__)


@appview.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("appview.prediction"))
    else:
    	return render_template(
        "home.html"
    )
        # return redirect(url_for("authview.login_page"))
@appview.route("/home")      
def home():
    return render_template(
        "home.html"
    )
@appview.route("/aboutus")
def aboutus():
    return render_template(
        "aboutus.html",
        title="Cardio Predict | Prediction",
        page_header="Cardio Predict",
    )
@appview.route("/getstarted")
def getstarted():
    return render_template(
        "aboutus.html",
        title="Cardio Predict | Prediction",
        page_header="Cardio Predict",
    )

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

@appview.route("/history")
@login_required
def session_history():
    try:
        user_history = UserHistory.query.filter_by(user=current_user).all()
        # import pdb
        # pdb.set_trace()
        print(user_history)
        return render_template("session_history.html", sessions=user_history)
    except:
        print(traceback.format_exc())
        return render_template(
        "aboutus.html",
        title="Cardio Predict | Prediction",
        page_header="Cardio Predict",
        )

@appview.route("/medhistory")
@login_required
def session_medhistory():
    try:
        medhistory = MedicalRecord.query.filter_by(user=current_user).all()
        
        # import pdb
        # pdb.set_trace()
        print(medhistory)
        return render_template("medhistory.html", sessions=medhistory)
    except:
        print(traceback.format_exc())
        return render_template(
        "medhistory.html",
        title="Cardio Predict | Prediction",
        page_header="Cardio Predict",
        )