#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lager, Bediener, Htparam

def prepare_s_stockin_1bl():

    prepare_cache ([Htparam])

    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    billdate = None
    fb_closedate = None
    m_closedate = None
    last_mdate = None
    last_fbdate = None
    fl_code1 = 0
    fl_code2 = 0
    ci_date = None
    t_l_lager_list = []
    temp_bediener_list = []
    l_lager = bediener = htparam = None

    t_l_lager = temp_bediener = None

    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    temp_bediener_list, Temp_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, fl_code1, fl_code2, ci_date, t_l_lager_list, temp_bediener_list, l_lager, bediener, htparam


        nonlocal t_l_lager, temp_bediener
        nonlocal t_l_lager_list, temp_bediener_list

        return {"f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "last_mdate": last_mdate, "last_fbdate": last_fbdate, "fl_code1": fl_code1, "fl_code2": fl_code2, "ci_date": ci_date, "t-l-lager": t_l_lager_list, "temp-bediener": temp_bediener_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    b_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    m_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    fb_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    m_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if billdate == None or billdate > get_current_date():
        billdate = get_current_date()
    else:

        if m_closedate != None:
            last_mdate = date_mdy(get_month(m_closedate) , 1, get_year(m_closedate)) - timedelta(days=1)

        if fb_closedate != None:
            last_fbdate = date_mdy(get_month(fb_closedate) , 1, get_year(fb_closedate)) - timedelta(days=1)

        if (billdate <= last_mdate) or (billdate <= last_fbdate):
            fl_code1 = 1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})

        if htparam.fdate != None and billdate <= htparam.fdate:
            fl_code2 = 1

            return generate_output()

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
        temp_bediener = Temp_bediener()
        temp_bediener_list.append(temp_bediener)

        buffer_copy(bediener, temp_bediener)

    return generate_output()