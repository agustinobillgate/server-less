from functions.additional_functions import *
import decimal
from models import Guest

def company_glist_btn_helpbl(gastnr:int):
    from_name = ""
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_name, guest


        return {"from_name": from_name}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()
    from_name = guest.name

    return generate_output()