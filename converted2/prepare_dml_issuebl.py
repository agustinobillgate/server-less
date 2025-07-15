#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.dml_issue_create_dml_listbl import dml_issue_create_dml_listbl
from models import L_artikel, L_lager, Hoteldpt, Htparam

def prepare_dml_issuebl(curr_dept:int):

    prepare_cache ([Htparam])

    mat_grp = 0
    price_decimal = 0
    billdate = None
    closedate = None
    over_proz = to_decimal("0.0")
    err_code = 0
    p_232 = False
    t_l_lager_data = []
    t_hoteldpt_data = []
    dml_list_data = []
    t_l_artikel_data = []
    l_artikel = l_lager = hoteldpt = htparam = None

    t_l_artikel = t_l_lager = t_hoteldpt = dml_list = None

    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)
    t_l_lager_data, T_l_lager = create_model_like(L_lager)
    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)
    dml_list_data, Dml_list = create_model("Dml_list", {"bezeich":string, "anzahl":Decimal, "geliefert":Decimal, "einzelpreis":Decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mat_grp, price_decimal, billdate, closedate, over_proz, err_code, p_232, t_l_lager_data, t_hoteldpt_data, dml_list_data, t_l_artikel_data, l_artikel, l_lager, hoteldpt, htparam
        nonlocal curr_dept


        nonlocal t_l_artikel, t_l_lager, t_hoteldpt, dml_list
        nonlocal t_l_artikel_data, t_l_lager_data, t_hoteldpt_data, dml_list_data

        return {"mat_grp": mat_grp, "price_decimal": price_decimal, "billdate": billdate, "closedate": closedate, "over_proz": over_proz, "err_code": err_code, "p_232": p_232, "t-l-lager": t_l_lager_data, "t-hoteldpt": t_hoteldpt_data, "dml-list": dml_list_data, "t-l-artikel": t_l_artikel_data}

    p_232 = get_output(htplogic(232))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    mat_grp = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})

    if htparam.fdate != None and billdate <= htparam.fdate:
        err_code = 1

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 403)]})
    over_proz =  to_decimal(htparam.fdecimal) / to_decimal("100")

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_data.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)
    dml_list_data, t_l_artikel_data = get_output(dml_issue_create_dml_listbl(curr_dept, billdate))

    return generate_output()