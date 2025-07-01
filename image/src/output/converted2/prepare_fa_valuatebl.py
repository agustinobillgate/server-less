#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Fa_grup, Fa_lager, Htparam

def prepare_fa_valuatebl():

    prepare_cache ([Htparam])

    price_decimal = 0
    last_acctdate = None
    mm = 0
    yy = 0
    from_month = ""
    maxnr = 0
    p_977 = ""
    p_224 = None
    lagerbuff_list = []
    t_fa_grup_list = []
    t_fa_lager_list = []
    fa_grup = fa_lager = htparam = None

    t_fa_grup = t_fa_lager = lagerbuff = None

    t_fa_grup_list, T_fa_grup = create_model_like(Fa_grup)
    t_fa_lager_list, T_fa_lager = create_model_like(Fa_lager)
    lagerbuff_list, Lagerbuff = create_model_like(Fa_lager)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, last_acctdate, mm, yy, from_month, maxnr, p_977, p_224, lagerbuff_list, t_fa_grup_list, t_fa_lager_list, fa_grup, fa_lager, htparam


        nonlocal t_fa_grup, t_fa_lager, lagerbuff
        nonlocal t_fa_grup_list, t_fa_lager_list, lagerbuff_list

        return {"price_decimal": price_decimal, "last_acctdate": last_acctdate, "mm": mm, "yy": yy, "from_month": from_month, "maxnr": maxnr, "p_977": p_977, "p_224": p_224, "lagerBuff": lagerbuff_list, "t-fa-grup": t_fa_grup_list, "t-fa-lager": t_fa_lager_list}

    def load_fa_lager():

        nonlocal price_decimal, last_acctdate, mm, yy, from_month, maxnr, p_977, p_224, lagerbuff_list, t_fa_grup_list, t_fa_lager_list, fa_grup, fa_lager, htparam


        nonlocal t_fa_grup, t_fa_lager, lagerbuff
        nonlocal t_fa_grup_list, t_fa_lager_list, lagerbuff_list

        for fa_lager in db_session.query(Fa_lager).order_by(Fa_lager.lager_nr).all():
            lagerbuff = Lagerbuff()
            lagerbuff_list.append(lagerbuff)

            buffer_copy(fa_lager, lagerbuff)
            maxnr = fa_lager.lager_nr
        maxnr = maxnr + 1
        lagerbuff = Lagerbuff()
        lagerbuff_list.append(lagerbuff)

        lagerbuff.lager_nr = maxnr
        lagerbuff.bezeich = ""

    p_224 = get_output(htpdate(224))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
    p_977 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 881)]})
    last_acctdate = htparam.fdate
    mm = get_month(last_acctdate)
    yy = get_year(last_acctdate)
    from_month = to_string(mm, "99") + to_string(yy, "9999")
    load_fa_lager()

    for fa_grup in db_session.query(Fa_grup).order_by(Fa_grup._recid).all():
        t_fa_grup = T_fa_grup()
        t_fa_grup_list.append(t_fa_grup)

        buffer_copy(fa_grup, t_fa_grup)

    for fa_lager in db_session.query(Fa_lager).order_by(Fa_lager._recid).all():
        t_fa_lager = T_fa_lager()
        t_fa_lager_list.append(t_fa_lager)

        buffer_copy(fa_lager, t_fa_lager)

    return generate_output()