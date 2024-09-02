from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lager, Htparam, Waehrung, L_hauptgrp

def prepare_fb_flash1bl():
    food = 0
    bev = 0
    date2 = None
    date1 = None
    bill_date = None
    double_currency = False
    foreign_nr = 0
    exchg_rate = 0
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    l_lager = htparam = waehrung = l_hauptgrp = None

    t_l_hauptgrp = t_l_lager = None

    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":str})
    t_l_lager_list, T_l_lager = create_model_like(L_lager)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal food, bev, date2, date1, bill_date, double_currency, foreign_nr, exchg_rate, t_l_lager_list, t_l_hauptgrp_list, l_lager, htparam, waehrung, l_hauptgrp


        nonlocal t_l_hauptgrp, t_l_lager
        nonlocal t_l_hauptgrp_list, t_l_lager_list
        return {"food": food, "bev": bev, "date2": date2, "date1": date1, "bill_date": bill_date, "double_currency": double_currency, "foreign_nr": foreign_nr, "exchg_rate": exchg_rate, "t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    food = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    bev = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    date2 = fdate
    date1 = date_mdy(get_month(date2) , 1, get_year(date2))

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

    for l_lager in db_session.query(L_lager).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_hauptgrp in db_session.query(L_hauptgrp).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    return generate_output()