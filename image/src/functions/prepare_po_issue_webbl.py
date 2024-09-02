from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_orderhdr, L_lager, Htparam, Bediener, L_lieferant, Parameters, L_artikel, Waehrung

def prepare_po_issue_webbl(pvilanguage:int, lief_nr:int, user_init:str, docu_nr:str):
    enforce_rflag = False
    show_price = False
    higherprice_flag = False
    disc_flag = False
    price_decimal = 0
    qty_flag = False
    qty_tol = 0
    crterm = 0
    lieferdatum = None
    bestellart = ""
    comments = ""
    supplier = ""
    deptname = ""
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    billdate = None
    fb_closedate = None
    m_closedate = None
    last_mdate = None
    last_fbdate = None
    err_code = 0
    t_amount = 0
    waehrung_wabkurz = ""
    exchg_rate = 0
    msg_str = ""
    ci_date = None
    t_l_orderhdr_list = []
    t_l_lager_list = []
    t_l_order_list = []
    l_order = l_orderhdr = l_lager = htparam = bediener = l_lieferant = parameters = l_artikel = waehrung = None

    t_l_order = t_l_orderhdr = t_l_lager = None

    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":str, "jahrgang":int, "alkoholgrad":decimal, "curr_disc":int, "curr_disc2":int, "curr_vat":int})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_lager_list, T_l_lager = create_model_like(L_lager)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal enforce_rflag, show_price, higherprice_flag, disc_flag, price_decimal, qty_flag, qty_tol, crterm, lieferdatum, bestellart, comments, supplier, deptname, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, err_code, t_amount, waehrung_wabkurz, exchg_rate, msg_str, ci_date, t_l_orderhdr_list, t_l_lager_list, t_l_order_list, l_order, l_orderhdr, l_lager, htparam, bediener, l_lieferant, parameters, l_artikel, waehrung


        nonlocal t_l_order, t_l_orderhdr, t_l_lager
        nonlocal t_l_order_list, t_l_orderhdr_list, t_l_lager_list
        return {"enforce_rflag": enforce_rflag, "show_price": show_price, "higherprice_flag": higherprice_flag, "disc_flag": disc_flag, "price_decimal": price_decimal, "qty_flag": qty_flag, "qty_tol": qty_tol, "crterm": crterm, "lieferdatum": lieferdatum, "bestellart": bestellart, "comments": comments, "supplier": supplier, "deptname": deptname, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "last_mdate": last_mdate, "last_fbdate": last_fbdate, "err_code": err_code, "t_amount": t_amount, "waehrung_wabkurz": waehrung_wabkurz, "exchg_rate": exchg_rate, "msg_str": msg_str, "ci_date": ci_date, "t-l-orderhdr": t_l_orderhdr_list, "t-l-lager": t_l_lager_list, "t-l-order": t_l_order_list}

    def cal_tamount():

        nonlocal enforce_rflag, show_price, higherprice_flag, disc_flag, price_decimal, qty_flag, qty_tol, crterm, lieferdatum, bestellart, comments, supplier, deptname, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, err_code, t_amount, waehrung_wabkurz, exchg_rate, msg_str, ci_date, t_l_orderhdr_list, t_l_lager_list, t_l_order_list, l_order, l_orderhdr, l_lager, htparam, bediener, l_lieferant, parameters, l_artikel, waehrung


        nonlocal t_l_order, t_l_orderhdr, t_l_lager
        nonlocal t_l_order_list, t_l_orderhdr_list, t_l_lager_list


        t_amount = 0

    def get_currency():

        nonlocal enforce_rflag, show_price, higherprice_flag, disc_flag, price_decimal, qty_flag, qty_tol, crterm, lieferdatum, bestellart, comments, supplier, deptname, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, err_code, t_amount, waehrung_wabkurz, exchg_rate, msg_str, ci_date, t_l_orderhdr_list, t_l_lager_list, t_l_order_list, l_order, l_orderhdr, l_lager, htparam, bediener, l_lieferant, parameters, l_artikel, waehrung


        nonlocal t_l_order, t_l_orderhdr, t_l_lager
        nonlocal t_l_order_list, t_l_orderhdr_list, t_l_lager_list

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == l_orderhdr.angebot_lief[2])).first()

        if waehrung:
            waehrung_wabkurz = waehrung.wabkurz
            exchg_rate = waehrung.ankauf / waehrung.einheit

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    if not l_orderhdr:
        err_code = 1

        return generate_output()
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 222)).first()
    enforce_rflag = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 350)).first()
    higherprice_flag = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 349)).first()

    if htparam.feldtyp != 4:
        disc_flag = False
    else:
        disc_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1010) &  (Htparam.paramgruppe == 21)).first()

    if htparam:
        qty_flag = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1011) &  (Htparam.paramgruppe == 21)).first()

        if htparam:
            qty_tol = htparam.finteger
    crterm = l_orderhdr.angebot_lief[1]

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

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
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    fb_closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    m_closedate = htparam.fdate

    if billdate == None or billdate > get_current_date():
        billdate = get_current_date()
    else:

        if m_closedate != None:
            last_mdate = date_mdy(get_month(m_closedate) , 1, get_year(m_closedate)) - 1

        if fb_closedate != None:
            last_fbdate = date_mdy(get_month(fb_closedate) , 1, get_year(fb_closedate)) - 1

        if (billdate <= last_mdate) or (billdate <= last_fbdate):
            msg_str = msg_str + chr(2) + "&W" + "Receiving Date might be incorrect (too old)," + chr(10) + "Please re_check it."

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 269)).first()

        if htparam.fdate != None and billdate <= htparam.fdate:
            msg_str = msg_str + chr(2) + "&W" + "Wrong receiving date (ParamNo 474):" + chr(10) + "Older than last transfer date to the G/L."

            return generate_output()
    cal_tamount()
    get_currency()

    for l_lager in db_session.query(L_lager).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_order in db_session.query(L_order).filter(
            (L_order.pos > 0) &  (L_order.loeschflag == 0) &  (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower())).all():
        t_l_order = T_l_order()
        t_l_order_list.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_order.artnr)).first()

        if l_artikel:
            t_l_order.a_bezeich = l_artikel.bezeich
            t_l_order.jahrgang = l_artikel.jahrgang
            t_l_order.alkoholgrad = l_artikel.alkoholgrad
            t_l_order.curr_disc = to_int(substring(t_l_order.quality, 0, 2)) * 100 +\
                    to_int(substring(t_l_order.quality, 3, 2))
            t_l_order.curr_vat = to_int(substring(t_l_order.quality, 6, 2)) * 100 +\
                    to_int(substring(t_l_order.quality, 9, 2))
            t_l_order.curr_disc2 = 0

        if l_artikel.lief_einheit > 1 and t_l_order.geliefert > 0:
            t_l_order.angebot_lief[0] = t_l_order.geliefert % l_artikel.lief_einheit
            t_l_order.geliefert = (t_l_order.geliefert - t_l_order.angebot_lief [0]) / l_artikel.lief_einheit

        if len(t_l_order.quality) >= 17:
            t_l_order.curr_disc2 = to_int(substring(t_l_order.quality, 12, 2)) * 100 + to_int(substring(t_l_order.quality, 15, 2))

    return generate_output()