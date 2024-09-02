from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener

def prepare_vip_listbl(user_init:str):
    ci_date = None
    show_rate = False
    p_297 = 0
    lnl_filepath = ""
    t_vipnr_list = []
    htparam = bediener = None

    t_vipnr = None

    t_vipnr_list, T_vipnr = create_model("T_vipnr", {"vip_nr1":int, "vip_nr2":int, "vip_nr3":int, "vip_nr4":int, "vip_nr5":int, "vip_nr6":int, "vip_nr7":int, "vip_nr8":int, "vip_nr9":int, "vip_nr10":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, show_rate, p_297, lnl_filepath, t_vipnr_list, htparam, bediener


        nonlocal t_vipnr
        nonlocal t_vipnr_list
        return {"ci_date": ci_date, "show_rate": show_rate, "p_297": p_297, "lnl_filepath": lnl_filepath, "t-vipnr": t_vipnr_list}

    def fill_vipnr():

        nonlocal ci_date, show_rate, p_297, lnl_filepath, t_vipnr_list, htparam, bediener


        nonlocal t_vipnr
        nonlocal t_vipnr_list


        t_vipnr = T_vipnr()
        t_vipnr_list.append(t_vipnr)


        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 700)).first()
        t_vipnr.vip_nr1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 701)).first()
        t_vipnr.vip_nr2 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 702)).first()
        t_vipnr.vip_nr3 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 703)).first()
        t_vipnr.vip_nr4 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 704)).first()
        t_vipnr.vip_nr5 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 705)).first()
        t_vipnr.vip_nr6 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 706)).first()
        t_vipnr.vip_nr7 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 707)).first()
        t_vipnr.vip_nr8 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 708)).first()
        t_vipnr.vip_nr9 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 712)).first()
        t_vipnr.vip_nr10 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 417)).first()

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, len(lnl_filepath) - 1, 1) != "\\":
            lnl_filepath = lnl_filepath + "\\"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 297)).first()
    p_297 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if substring(bediener.permissions, 34, 1) != "0":
        show_rate = True
    fill_vipnr()

    return generate_output()