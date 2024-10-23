from functions.additional_functions import *
import decimal
from models import Akthdr

akthdr1_list, Akthdr1 = create_model_like(Akthdr)

def chg_akthdr_btn_exitbl(akthdr1_list:[Akthdr1]):
    akthdr = None

    akthdr1 = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal akthdr
        nonlocal akthdr1_list


        nonlocal akthdr1
        nonlocal akthdr1_list
        return {}

    akthdr1 = query(akthdr1_list, first=True)

    akthdr = db_session.query(Akthdr).filter(
             (Akthdr.aktnr == akthdr1.aktnr)).first()
    buffer_copy(akthdr1, akthdr)

    return generate_output()