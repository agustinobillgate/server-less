from functions.additional_functions import *
import decimal
from models import Guest

def res_fill_gcfemailbl(inp_gastnr:int, email_str:str):
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest


        return {}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == inp_gastnr)).first()

    guest = db_session.query(Guest).first()
    guest.email_adr = email_str

    guest = db_session.query(Guest).first()

    return generate_output()