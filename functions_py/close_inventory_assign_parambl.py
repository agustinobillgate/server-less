#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def close_inventory_assign_parambl(user_init:string, inv_type:int):

    prepare_cache ([Htparam])

    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam
        nonlocal user_init, inv_type

        return {}


    if inv_type == 1:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 224).with_for_update().first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
        pass

    elif inv_type == 2:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 221).with_for_update().first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
        pass

    elif inv_type == 3:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 221).with_for_update().first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
        pass

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 224).with_for_update().first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
        pass

    return generate_output()