from functions.additional_functions import *
import decimal
from models import Printer

def rarticle_admin_bondruckernrbl(h_bondruckernr:int, h_bondrucker:int):
    flag = 0
    printer = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, printer


        return {"flag": flag}


    printer = db_session.query(Printer).filter(
            (Printer.nr == h_bondruckernr) &  (Printer.bondrucker)).first()

    if not printer and h_bondrucker != 0:
        flag = 1

    return generate_output()