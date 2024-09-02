from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Paramtext

def prepare_avail_roombl():
    ci_date = None
    setup_combo = ""
    view_combo = ""
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, setup_combo, view_combo, paramtext


        return {"ci_date": ci_date, "setup_combo": setup_combo, "view_combo": view_combo}

    ci_date = get_output(htpdate(87))

    for paramtext in db_session.query(Paramtext).filter(
            (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():
        setup_combo = setup_combo + paramtext.ptexte + ";"

    for paramtext in db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 230)).all():
        view_combo = view_combo + paramtext.ptexte + ";"

    return generate_output()