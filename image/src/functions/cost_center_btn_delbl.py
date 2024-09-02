from functions.additional_functions import *
import decimal
from models import Parameters

def cost_center_btn_delbl(rec_id:int):
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters


        return {}


    parameters = db_session.query(Parameters).filter(
            (Parameters._recid == rec_id)).first()
    db_session.delete(parameters)

    return generate_output()