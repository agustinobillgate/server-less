from functions.additional_functions import *
import decimal
from models import Parameters

def cost_budget_update_costlistbl(cost_list_rec_id:int, name1:str):
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal cost_list_rec_id, name1


        return {}

    def update_costlist():

        nonlocal parameters
        nonlocal cost_list_rec_id, name1

        parameters = db_session.query(Parameters).filter(
                 (Parameters._recid == cost_list_rec_id)).first()
        parameters.vstring = name1


    update_costlist()

    return generate_output()