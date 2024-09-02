from functions.additional_functions import *
import decimal
from models import Parameters

def if_country1_update_costlistbl(cost_list_rec_id:int, zone1:str, grace1:int, wday1:int, ftime1:int, ttime1:int, tdura1:int, dura1:int, cost1:decimal):
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters


        return {}

    def update_costlist():

        nonlocal parameters

        s:str = ""

        parameters = db_session.query(Parameters).filter(
                (Parameters._recid == cost_list_rec_id)).first()
        parameters.vstring = to_string(grace1) + ";" + to_string(wday1) + ";" + to_string(ftime1, "9999") + ";" + to_string(ttime1, "9999") + ";" + to_string(tdura1) + ";" + to_string(dura1) + ";" + to_string(cost1, ">>>>>>9.99") + ";" + s

        parameters = db_session.query(Parameters).first()

    update_costlist()

    return generate_output()