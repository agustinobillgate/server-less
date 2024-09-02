from functions.additional_functions import *
import decimal
from models import Fa_kateg, Fa_artikel

def fa_kategadmin_btn_delartbl(rec_id:int):
    do_it = False
    fa_kateg = fa_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, fa_kateg, fa_artikel


        return {"do_it": do_it}


    fa_kateg = db_session.query(Fa_kateg).filter(
            (Fa_kateg._recid == rec_id)).first()

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.katnr == fa_kateg.katnr)).first()

    if fa_artikel:
        do_it = False
    else:

        fa_kateg = db_session.query(Fa_kateg).first()
        db_session.delete(fa_kateg)


    return generate_output()