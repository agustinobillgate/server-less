from functions.additional_functions import *
import decimal
from models import Parameters

def cost_budget_btn_del1bl(cost_list_rec_id:int):
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters


        return {}


    parameters = db_session.query(Parameters).filter(
            (Parameters._recid == cost_list_rec_id)).first()
    db_session.delete(parameters)

    return generate_output()