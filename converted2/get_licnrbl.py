from functions.additional_functions import *
import decimal
from models import Paramtext

def get_licnrbl():
    licnr = ""
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal licnr, paramtext

        return {"licnr": licnr}


    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext:
        licnr = paramtext.ptexte

    return generate_output()