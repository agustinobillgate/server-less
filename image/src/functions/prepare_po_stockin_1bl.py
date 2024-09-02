from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, L_order, L_orderhdr, L_artikel, Htparam, Bediener, L_lieferant, Parameters, Waehrung

def prepare_po_stockin_1bl(lief_nr:int, docu_nr:str, user_init:str):
    enforce_rflag = False
    show_price = False
    qty_flag = False
    qty_tol = 0
    higherprice_flag = False
    disc_flag = False
    crterm = 0
    price_decimal = 0
    lieferdatum = None
    bestellart = ""
    comments = ""
    supplier = ""
    deptname = ""
    billdate = None
    last_mdate = None
    last_fbdate = None
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    fb_closedate = None
    m_closedate = None
    t_amount = 0
    order_amt = 0
    exchg_rate = 0
    waehrung_wabkurz = ""
    fl_code = 0
    fl_code1 = 0
    avail_param = False
    fl_warn = False
    avail_waehrung = False
    ci_date = None
    rcv_po = False
    t_l_order_list = []
    t_l_orderhdr_list = []
    q_20_list = []
    queasy = l_order = l_orderhdr = l_artikel = htparam = bediener = l_lieferant = parameters = waehrung = None

    q_20 = t_l_order = t_l_orderhdr = t_l_artikel = None

    q_20_list, Q_20 = create_model_like(Queasy)
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "art_bezeich":str, "jahrgang":int, "alkoholgrad":decimal, "lief_einheit":decimal})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal enforce_rflag, show_price, qty_flag, qty_tol, higherprice_flag, disc_flag, crterm, price_decimal, lieferdatum, bestellart, comments, supplier, deptname, billdate, last_mdate, last_fbdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, t_amount, order_amt, exchg_rate, waehrung_wabkurz, fl_code, fl_code1, avail_param, fl_warn, avail_waehrung, ci_date, rcv_po, t_l_order_list, t_l_orderhdr_list, q_20_list, queasy, l_order, l_orderhdr, l_artikel, htparam, bediener, l_lieferant, parameters, waehrung


        nonlocal q_20, t_l_order, t_l_orderhdr, t_l_artikel
        nonlocal q_20_list, t_l_order_list, t_l_orderhdr_list, t_l_artikel_list
        return {"enforce_rflag": enforce_rflag, "show_price": show_price, "qty_flag": qty_flag, "qty_tol": qty_tol, "higherprice_flag": higherprice_flag, "disc_flag": disc_flag, "crterm": crterm, "price_decimal": price_decimal, "lieferdatum": lieferdatum, "bestellart": bestellart, "comments": comments, "supplier": supplier, "deptname": deptname, "billdate": billdate, "last_mdate": last_mdate, "last_fbdate": last_fbdate, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "t_amount": t_amount, "order_amt": order_amt, "exchg_rate": exchg_rate, "waehrung_wabkurz": waehrung_wabkurz, "fl_code": fl_code, "fl_code1": fl_code1, "avail_param": avail_param, "fl_warn": fl_warn, "avail_waehrung": avail_waehrung, "ci_date": ci_date, "rcv_po": rcv_po, "t-l-order": t_l_order_list, "t-l-orderhdr": t_l_orderhdr_list, "q-20": q_20_list}

    def cal_tamount():

        nonlocal enforce_rflag, show_price, qty_flag, qty_tol, higherprice_flag, disc_flag, crterm, price_decimal, lieferdatum, bestellart, comments, supplier, deptname, billdate, last_mdate, last_fbdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, t_amount, order_amt, exchg_rate, waehrung_wabkurz, fl_code, fl_code1, avail_param, fl_warn, avail_waehrung, ci_date, rcv_po, t_l_order_list, t_l_orderhdr_list, q_20_list, queasy, l_order, l_orderhdr, l_artikel, htparam, bediener, l_lieferant, parameters, waehrung


        nonlocal q_20, t_l_order, t_l_orderhdr, t_l_artikel
        nonlocal q_20_list, t_l_order_list, t_l_orderhdr_list, t_l_artikel_list


        t_amount = 0
        order_amt = 0

        l_order = db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).first()
        while None != l_order:
            order_amt = order_amt + l_order.warenwert

            l_order = db_session.query(L_order).filter(
                    (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).first()

    def get_currency():

        nonlocal enforce_rflag, show_price, qty_flag, qty_tol, higherprice_flag, disc_flag, crterm, price_decimal, lieferdatum, bestellart, comments, supplier, deptname, billdate, last_mdate, last_fbdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, t_amount, order_amt, exchg_rate, waehrung_wabkurz, fl_code, fl_code1, avail_param, fl_warn, avail_waehrung, ci_date, rcv_po, t_l_order_list, t_l_orderhdr_list, q_20_list, queasy, l_order, l_orderhdr, l_artikel, htparam, bediener, l_lieferant, parameters, waehrung


        nonlocal q_20, t_l_order, t_l_orderhdr, t_l_artikel
        nonlocal q_20_list, t_l_order_list, t_l_orderhdr_list, t_l_artikel_list

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == l_orderhdr.angebot_lief[2])).first()

        if waehrung:
            waehrung_wabkurz = waehrung.wabkurz
            avail_waehrung = True
            exchg_rate = waehrung.ankauf / waehrung.einheit


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr.docu_nr == docu_nr no_wait)).first()

    if l_orderhdr:
        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_list.append(t_l_orderhdr)

        buffer_copy(l_orderhdr, t_l_orderhdr)
        t_l_orderhdr.rec_id = l_orderhdr._recid

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 222)).first()
    enforce_rflag = flogical

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1010) &  (Htparam.paramgruppe == 21)).first()

    if htparam:
        qty_flag = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1011) &  (Htparam.paramgruppe == 21)).first()

        if htparam:
            qty_tol = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 350)).first()
    higherprice_flag = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 349)).first()

    if htparam.feldtyp != 4:
        disc_flag = False
    else:
        disc_flag = htparam.flogical

    if not l_orderhdr:
        fl_code = 1

        return generate_output()

    if l_orderhdr.gedruckt == None and enforce_rflag:
        fl_code1 = 1
    crterm = l_orderhdr.angebot_lief[1]

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()
    lieferdatum = l_orderhdr.lieferdatum
    bestellart = l_orderhdr.bestellart
    comments = l_orderhdr.lief_fax[2]
    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort

    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

    if parameters:
        deptname = parameters.vstring
        avail_param = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    if billdate == None or billdate > get_current_date():
        billdate = get_current_date()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()

        if htparam.fdate != None:
            last_mdate = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate)) - 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()

        if htparam.fdate != None:
            last_fbdate = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate)) - 1

        if (billdate <= last_mdate) or (billdate <= last_fbdate):
            fl_warn = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 269)).first()

        if htparam.fdate != None and billdate <= htparam.fdate:
            fl_code = 2

            return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    f_endkum = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    b_endkum = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 268)).first()
    m_endkum = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    fb_closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    m_closedate = htparam.fdate
    cal_tamount()
    get_currency()

    l_order = db_session.query(L_order).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).first()
    while None != l_order:
        t_l_order = T_l_order()
        t_l_order_list.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_order.artnr)).first()
        t_l_order.art_bezeich = l_artikel.bezeich
        t_l_order.jahrgang = l_artikel.jahrgang
        t_l_order.alkoholgrad = l_artikel.alkoholgrad
        t_l_order.lief_einheit = l_artikel.lief_einheit

        l_order = db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).first()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 20)).all():
        q_20 = Q_20()
        q_20_list.append(q_20)

        buffer_copy(queasy, q_20)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1354) &  (func.lower(Htparam.bezeich) != "not used")).first()

    if htparam:
        rcv_po = htparam.flogical

    return generate_output()