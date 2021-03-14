import os
import joblib

from exceptions import FormValidationError
from config import constants, Config
from models.user import User
from models.medicalrecord import MedicalRecord

class PredictionController:
    def __init__(self, form_data:dict) -> None:
        self._form_data = form_data

    def __value_predictor(self, to_predict_list, size):
        print(to_predict_list)
        loaded_model = joblib.load(os.path.join(Config.BASE_DIR, "app", "models", "model9.pkl"))
        result = loaded_model.predict([to_predict_list])
        return result[0]
        
    
    def predict(self) -> bool:
        to_predict_list = list(self._form_data.values())
        to_predict_list = list(map(float, to_predict_list))

        if len(to_predict_list) == 11:
            result = self.__value_predictor(to_predict_list, 11)
        else:
            print(self._form_data)
            raise FormValidationError("Incorrect number of fields received")
        
        return result

    def save_to_db(self, user:User):
        _data = self._form_data.copy()
        _data["age"] = int(_data["age"])
        
        for _field in {"weight", "height", "systolic_bp", "diastolic_bp"}:
            _data[_field] = float(_data[_field])
        
        _data["gender"] = constants.GENDER.get(_data["gender"])

        for _field in {"cholesterol_level", "blood_glucose_level"}:
            _data[_field] = constants.LEVELS.get(_data[_field])
        
        for _field in {"smoking", "alcohol", "physical_activity"}:
            _data[_field] = constants.CHOICE.get(_data[_field])

        _record = MedicalRecord(**_data)
        _record.user = user
        _record.save()
        
        return _record
