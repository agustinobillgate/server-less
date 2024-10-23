from functions.additional_functions import *
import decimal
from models import Htparam

def close_inventory_assign_parambl(user_init:str, inv_type:int):
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam
        nonlocal user_init, inv_type


        return {}


    if inv_type == 1:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 224)).first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    elif inv_type == 2:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 221)).first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    elif inv_type == 3:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 221)).first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 224)).first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    return generate_output()