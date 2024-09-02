from functions.additional_functions import *
import decimal
from models import Mc_types, Mc_guest, Mc_fee

def mc_gcf0_readbl(case_type:int, int1:int):
    flag = False
    mc_types = mc_guest = mc_fee = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, mc_types, mc_guest, mc_fee


        return {"flag": flag}


    if case_type == 1:

        mc_types = db_session.query(Mc_types).filter(
                (Mc_types.nr == int1)).first()

        if mc_types:
            flag = True

    elif case_type == 2:

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.gastnr == int1)).first()

        mc_fee = db_session.query(Mc_fee).filter(
                (Mc_fee.key == 1) &  (Mc_fee.gastnr == mc_guest.gastnr) &  (Mc_fee.bis_datum == mc_guest.tdate)).first()

        if mc_fee and mc_fee.bezahlt != 0:
            flag = True

    return generate_output()