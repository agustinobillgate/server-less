from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from functions.dml_issue_create_dml_listbl import dml_issue_create_dml_listbl
from models import L_artikel, L_lager, Hoteldpt, Htparam

def prepare_dml_issuebl(curr_dept:int):
    mat_grp = 0
    price_decimal = 0
    billdate = None
    closedate = None
    over_proz = 0
    err_code = 0
    p_232 = False
    t_l_lager_list = []
    t_hoteldpt_list = []
    dml_list_list = []
    t_l_artikel_list = []
    l_artikel = l_lager = hoteldpt = htparam = None

    t_l_artikel = t_l_lager = t_hoteldpt = dml_list = None

    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)
    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    dml_list_list, Dml_list = create_model("Dml_list", {"bezeich":str, "anzahl":decimal, "geliefert":decimal, "einzelpreis":decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mat_grp, price_decimal, billdate, closedate, over_proz, err_code, p_232, t_l_lager_list, t_hoteldpt_list, dml_list_list, t_l_artikel_list, l_artikel, l_lager, hoteldpt, htparam


        nonlocal t_l_artikel, t_l_lager, t_hoteldpt, dml_list
        nonlocal t_l_artikel_list, t_l_lager_list, t_hoteldpt_list, dml_list_list
        return {"mat_grp": mat_grp, "price_decimal": price_decimal, "billdate": billdate, "closedate": closedate, "over_proz": over_proz, "err_code": err_code, "p_232": p_232, "t-l-lager": t_l_lager_list, "t-hoteldpt": t_hoteldpt_list, "dml-list": dml_list_list, "t-l-artikel": t_l_artikel_list}

    p_232 = get_output(htplogic(232))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 268)).first()
    mat_grp = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 269)).first()

    if htparam.fdate != None and billdate <= htparam.fdate:
        err_code = 1

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 403)).first()
    over_proz = htparam.fdecimal / 100

    for l_lager in db_session.query(L_lager).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)
    dml_list_list, t_l_artikel_list = get_output(dml_issue_create_dml_listbl(curr_dept, billdate))

    return generate_output()