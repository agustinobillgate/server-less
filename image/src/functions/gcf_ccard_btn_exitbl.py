from functions.additional_functions import *
import decimal
from models import Guest

def gcf_ccard_btn_exitbl(gastnr:int, ausweis_nr2:str):
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest


        return {}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()
    guest.ausweis_nr2 = ausweis_nr2

    guest = db_session.query(Guest).first()

    return generate_output()