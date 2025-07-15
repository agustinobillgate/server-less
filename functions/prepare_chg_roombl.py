#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_raum, Bk_rset, Bk_setup, Bk_func, Bk_reser, Htparam

def prepare_chg_roombl():

    prepare_cache ([Htparam])

    braum_data = []
    bset_data = []
    bsetup_data = []
    bfunc_data = []
    breser_data = []
    bill_date:date = None
    bk_raum = bk_rset = bk_setup = bk_func = bk_reser = htparam = None

    braum = bset = bsetup = bfunc = breser = None

    braum_data, Braum = create_model_like(Bk_raum, {"rmflag":bool})
    bset_data, Bset = create_model_like(Bk_rset)
    bsetup_data, Bsetup = create_model_like(Bk_setup)
    bfunc_data, Bfunc = create_model_like(Bk_func)
    breser_data, Breser = create_model_like(Bk_reser)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal braum_data, bset_data, bsetup_data, bfunc_data, breser_data, bill_date, bk_raum, bk_rset, bk_setup, bk_func, bk_reser, htparam


        nonlocal braum, bset, bsetup, bfunc, breser
        nonlocal braum_data, bset_data, bsetup_data, bfunc_data, breser_data

        return {"braum": braum_data, "bset": bset_data, "bsetup": bsetup_data, "bfunc": bfunc_data, "breser": breser_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        braum = Braum()
        braum_data.append(braum)

        buffer_copy(bk_raum, braum)

    for bk_rset in db_session.query(Bk_rset).order_by(Bk_rset._recid).all():
        bset = Bset()
        bset_data.append(bset)

        buffer_copy(bk_rset, bset)

    for bk_setup in db_session.query(Bk_setup).order_by(Bk_setup._recid).all():
        bsetup = Bsetup()
        bsetup_data.append(bsetup)

        buffer_copy(bk_setup, bsetup)

    for bk_func in db_session.query(Bk_func).order_by(Bk_func._recid).all():
        bfunc = Bfunc()
        bfunc_data.append(bfunc)

        buffer_copy(bk_func, bfunc)

    for bk_reser in db_session.query(Bk_reser).filter(
             (Bk_reser.datum >= bill_date)).order_by(Bk_reser._recid).all():
        breser = Breser()
        breser_data.append(breser)

        buffer_copy(bk_reser, breser)

    return generate_output()