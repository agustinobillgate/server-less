from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, L_hauptgrp

def prepare_fb_reconsile1bl():
    food = 0
    bev = 0
    ldry = 0
    dstore = 0
    to_date = None
    from_date = None
    bill_date = None
    foreign_nr = 0
    double_currency = False
    exchg_rate = 0
    t_l_hauptgrp_list = []
    htparam = waehrung = l_hauptgrp = None

    t_l_hauptgrp = None

    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal food, bev, ldry, dstore, to_date, from_date, bill_date, foreign_nr, double_currency, exchg_rate, t_l_hauptgrp_list, htparam, waehrung, l_hauptgrp


        nonlocal t_l_hauptgrp
        nonlocal t_l_hauptgrp_list
        return {"food": food, "bev": bev, "ldry": ldry, "dstore": dstore, "to_date": to_date, "from_date": from_date, "bill_date": bill_date, "foreign_nr": foreign_nr, "double_currency": double_currency, "exchg_rate": exchg_rate, "t-l-hauptgrp": t_l_hauptgrp_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    food = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    bev = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1081)).first()
    ldry = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1082)).first()
    dstore = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    to_date = fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam.flogical:
        double_currency = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr
            exchg_rate = waehrung.ankauf / waehrung.einheit
        else:
            exchg_rate = 1

    for l_hauptgrp in db_session.query(L_hauptgrp).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        t_l_hauptgrp.endkum = l_hauptgrp.endkum
        t_l_hauptgrp.bezeich = l_hauptgrp.bezeich

    return generate_output()