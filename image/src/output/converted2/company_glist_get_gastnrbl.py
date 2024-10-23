from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest

def company_glist_get_gastnrbl(from_name:str):
    curr_gastnr = 0
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_gastnr, guest
        nonlocal from_name


        return {"from_name": from_name, "curr_gastnr": curr_gastnr}


    guest = db_session.query(Guest).filter(
             (func.lower(Guest.name) == (from_name).lower()) & (Guest.gastnr > 0)).first()

    if not guest and from_name != "":
        curr_gastnr = 0
    else:
        curr_gastnr = guest.gastnr
        from_name = guest.name

    return generate_output()