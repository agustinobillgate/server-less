from functions.additional_functions import *
import decimal
from models import Parameters

def if_country1_update_zonelistbl(zone_list_rec_id:int, city1:str, acode1:str, s:str):
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters


        return {}

    def update_zonelist():

        nonlocal parameters

        parameters = db_session.query(Parameters).filter(
                (Parameters._recid == zone_list_rec_id)).first()
        parameters.vstring = city1 + ";" + acode1 + ";" + s

        parameters = db_session.query(Parameters).first()

    update_zonelist()

    return generate_output()