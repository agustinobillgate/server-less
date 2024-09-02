from functions.additional_functions import *
import decimal
from models import Guest

def res_fill_gcfphonebl(inp_gastnr:int, phone_str:str):
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest


        return {}


    guest = db_session.query(Guest).filter(
                (Guest.gastnr == inp_gastnr)).first()

    if guest:

        guest = db_session.query(Guest).first()
        guest.mobil_telefon = phone_str

        guest = db_session.query(Guest).first()


    return generate_output()