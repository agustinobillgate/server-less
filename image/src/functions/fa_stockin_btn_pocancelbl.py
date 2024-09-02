from functions.additional_functions import *
import decimal
from models import Fa_op, Fa_artikel, L_kredit

def fa_stockin_btn_pocancelbl(rec_id:int):
    t_depn_wert = 0
    err_flag = 0
    fa_op = fa_artikel = l_kredit = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_depn_wert, err_flag, fa_op, fa_artikel, l_kredit


        return {"t_depn_wert": t_depn_wert, "err_flag": err_flag}


    fa_op = db_session.query(Fa_op).filter(
            (Fa_op._recid == rec_id)).first()

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == fa_op.nr)).first()

    if fa_artikel.depn_wert != 0:
        t_depn_wert = fa_artikel.depn_wert
        err_flag = 1
    else:

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit.name == fa_op.lscheinnr) &  (L_kredit.lief_nr == fa_op.lief_nr) &  (L_kredit.opart >= 1)).first()

        if l_kredit:
            err_flag = 2
        else:
            err_flag = 3

    return generate_output()