#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_raum, Bk_rset, Bk_setup, Bk_func, Bk_reser, Htparam

def prepare_chg_roombl():

    prepare_cache ([Htparam])

    braum_list = []
    bset_list = []
    bsetup_list = []
    bfunc_list = []
    breser_list = []
    bill_date:date = None
    bk_raum = bk_rset = bk_setup = bk_func = bk_reser = htparam = None

    braum = bset = bsetup = bfunc = breser = None

    braum_list, Braum = create_model_like(Bk_raum, {"rmflag":bool})
    bset_list, Bset = create_model_like(Bk_rset)
    bsetup_list, Bsetup = create_model_like(Bk_setup)
    bfunc_list, Bfunc = create_model_like(Bk_func)
    breser_list, Breser = create_model_like(Bk_reser)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal braum_list, bset_list, bsetup_list, bfunc_list, breser_list, bill_date, bk_raum, bk_rset, bk_setup, bk_func, bk_reser, htparam


        nonlocal braum, bset, bsetup, bfunc, breser
        nonlocal braum_list, bset_list, bsetup_list, bfunc_list, breser_list

        return {"braum": braum_list, "bset": bset_list, "bsetup": bsetup_list, "bfunc": bfunc_list, "breser": breser_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        braum = Braum()
        braum_list.append(braum)

        buffer_copy(bk_raum, braum)

    for bk_rset in db_session.query(Bk_rset).order_by(Bk_rset._recid).all():
        bset = Bset()
        bset_list.append(bset)

        buffer_copy(bk_rset, bset)

    for bk_setup in db_session.query(Bk_setup).order_by(Bk_setup._recid).all():
        bsetup = Bsetup()
        bsetup_list.append(bsetup)

        buffer_copy(bk_setup, bsetup)

    for bk_func in db_session.query(Bk_func).order_by(Bk_func._recid).all():
        bfunc = Bfunc()
        bfunc_list.append(bfunc)

        buffer_copy(bk_func, bfunc)

    for bk_reser in db_session.query(Bk_reser).filter(
             (Bk_reser.datum >= bill_date)).order_by(Bk_reser._recid).all():
        breser = Breser()
        breser_list.append(breser)

        buffer_copy(bk_reser, breser)

    return generate_output()