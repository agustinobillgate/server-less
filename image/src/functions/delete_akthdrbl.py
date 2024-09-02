from functions.additional_functions import *
import decimal
from models import Akthdr

def delete_akthdrbl(case_type:int, aktnr:int):
    success_flag = False
    akthdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, akthdr


        return {"success_flag": success_flag}


    if case_type == 1:

        akthdr = db_session.query(Akthdr).filter(
                (Akthdr.aktnr == aktnr)).first()

        if akthdr:
            db_session.delete(akthdr)

            success_flag = True

    return generate_output()