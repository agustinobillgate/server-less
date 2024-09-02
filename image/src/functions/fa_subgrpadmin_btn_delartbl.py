from functions.additional_functions import *
import decimal
from models import Fa_grup, Fa_artikel

def fa_subgrpadmin_btn_delartbl(rec_id:int):
    do_it = False
    fa_grup = fa_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, fa_grup, fa_artikel


        return {"do_it": do_it}


    fa_grup = db_session.query(Fa_grup).filter(
            (Fa_grup._recid == rec_id)).first()

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.gnr == fa_grup.gnr)).first()

    if fa_artikel:
        do_it = False
    else:

        fa_grup = db_session.query(Fa_grup).first()
        db_session.delete(fa_grup)


    return generate_output()