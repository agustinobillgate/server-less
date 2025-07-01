#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic

def intevent(ev_type:int, zinr:string, parms:string):
    doevent:bool = False
    parms_mapping:string = ""

    db_session = local_storage.db_session

    def generate_output():
        nonlocal doevent, parms_mapping
        nonlocal ev_type, zinr, parms

        return {}


    if parms.lower()  == ("Activate!").lower() :
        parms_mapping = "My Checkin!"

    elif parms.lower()  == ("Manual Checkin!").lower() :
        parms_mapping = "My Checkin!"

    elif parms.lower()  == ("Deactivate!").lower() :
        parms_mapping = "My Checkout!"

    elif parms.lower()  == ("Manual Checkout!").lower() :
        parms_mapping = "My Checkout!"
    else:
        parms_mapping = parms
    doevent = get_output(htplogic(398))

    if doevent:
        pass
    doevent = get_output(htplogic(359))

    if doevent:
        pass
    doevent = get_output(htplogic(358))

    if doevent and ev_type >= 1 and ev_type <= 3:
        pass

    return generate_output()