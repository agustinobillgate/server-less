#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.dml_stockin_create_dml_listbl import dml_stockin_create_dml_listbl
from models import Hoteldpt, L_lager, Bediener, Htparam

def prepare_dml_stockinbl(curr_dept:int):

    prepare_cache ([Htparam])

    price_decimal = 0
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    billdate = None
    fb_closedate = None
    m_closedate = None
    over_proz = to_decimal("0.0")
    flag_error = False
    p_232 = False
    dml_list_list = []
    t_hoteldpt_list = []
    t_l_lager_list = []
    t_bediener_list = []
    hoteldpt = l_lager = bediener = htparam = None

    dml_list = t_hoteldpt = t_l_lager = t_bediener = None

    dml_list_list, Dml_list = create_model("Dml_list", {"bezeich":string, "anzahl":Decimal, "geliefert":Decimal, "einzelpreis":Decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":string})
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    t_bediener_list, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, over_proz, flag_error, p_232, dml_list_list, t_hoteldpt_list, t_l_lager_list, t_bediener_list, hoteldpt, l_lager, bediener, htparam
        nonlocal curr_dept


        nonlocal dml_list, t_hoteldpt, t_l_lager, t_bediener
        nonlocal dml_list_list, t_hoteldpt_list, t_l_lager_list, t_bediener_list

        return {"price_decimal": price_decimal, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "over_proz": over_proz, "flag_error": flag_error, "p_232": p_232, "dml-list": dml_list_list, "t-hoteldpt": t_hoteldpt_list, "t-l-lager": t_l_lager_list, "t-bediener": t_bediener_list}

    p_232 = get_output(htplogic(232))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 403)]})
    over_proz =  to_decimal(htparam.fdecimal) / to_decimal("100")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})

    if htparam.fdate != None and billdate <= htparam.fdate:
        flag_error = True

        return generate_output()
    dml_list_list = get_output(dml_stockin_create_dml_listbl(curr_dept, billdate))

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    return generate_output()