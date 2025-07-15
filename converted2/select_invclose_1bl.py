#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import L_ophis, Htparam, L_artikel

def select_invclose_1bl():

    prepare_cache ([L_ophis, Htparam])

    fb_close_date = None
    mat_close_date = None
    last_journ_transgl = None
    flag_fb = False
    flag_mat = False
    partial = False
    last_rcv_transgl:date = None
    last_date:date = None
    bill_date:date = None
    tmp_date:date = None
    tmp_month:int = 0
    l_ophis = htparam = l_artikel = None

    ophis_fnb = ophis_mat = None

    Ophis_fnb = create_buffer("Ophis_fnb",L_ophis)
    Ophis_mat = create_buffer("Ophis_mat",L_ophis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fb_close_date, mat_close_date, last_journ_transgl, flag_fb, flag_mat, partial, last_rcv_transgl, last_date, bill_date, tmp_date, tmp_month, l_ophis, htparam, l_artikel
        nonlocal ophis_fnb, ophis_mat


        nonlocal ophis_fnb, ophis_mat

        return {"fb_close_date": fb_close_date, "mat_close_date": mat_close_date, "last_journ_transgl": last_journ_transgl, "flag_fb": flag_fb, "flag_mat": flag_mat, "partial": partial}

    fb_close_date = get_output(htpdate(224))
    mat_close_date = get_output(htpdate(221))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1035)]})

    if htparam:
        last_journ_transgl = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})

    if htparam:
        last_rcv_transgl = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1360)]})

    if htparam and htparam.bezeichnung.lower()  != ("not used").lower() :
        partial = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    if get_month(bill_date) == 12:
        tmp_date = date_mdy(1, 1, get_year(bill_date) + timedelta(days=1))
        last_date = tmp_date - timedelta(days=1)


    else:
        tmp_month = get_month(bill_date) + 1
        tmp_date = date_mdy(tmp_month, 1, get_year(bill_date))
        last_date = tmp_date - timedelta(days=1)

    if last_journ_transgl != None and last_journ_transgl < last_date:
        flag_fb = False
        flag_mat = False

    if last_rcv_transgl != None and last_rcv_transgl < last_date:
        flag_fb = False
        flag_mat = False

    if fb_close_date == last_journ_transgl:
        flag_fb = True

        for ophis_fnb in db_session.query(Ophis_fnb).filter(
                 (get_month(Ophis_fnb.datum) == get_month(fb_close_date)) & (get_year(Ophis_fnb.datum) == get_year(fb_close_date))).order_by(Ophis_fnb._recid).yield_per(100):

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, ophis_fnb.artnr)],"endkum": [(le, 2)]})

            if l_artikel:
                flag_fb = False


                break
    else:
        flag_fb = False

    if mat_close_date == last_journ_transgl:
        flag_mat = True

        for ophis_mat in db_session.query(Ophis_mat).filter(
                 (get_month(Ophis_mat.datum) == get_month(mat_close_date)) & (get_year(Ophis_mat.datum) == get_year(mat_close_date))).order_by(Ophis_mat._recid).yield_per(100):

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, ophis_mat.artnr)],"endkum": [(gt, 2)]})

            if l_artikel:
                flag_mat = False


                break
    else:
        flag_mat = False

    return generate_output()