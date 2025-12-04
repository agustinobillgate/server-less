#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, L_order, L_orderhdr, L_artikel, Htparam, Bediener, L_lieferant, Parameters, Waehrung

def prepare_po_stockin_1bl(lief_nr:int, docu_nr:string, user_init:string):

    prepare_cache ([L_artikel, Htparam, Bediener, L_lieferant, Parameters, Waehrung])

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
    t_amount = to_decimal("0.0")
    order_amt = to_decimal("0.0")
    exchg_rate = 1
    waehrung_wabkurz = ""
    fl_code = 0
    fl_code1 = 0
    avail_param = False
    fl_warn = False
    avail_waehrung = False
    ci_date = None
    rcv_po = False
    t_l_order_data = []
    t_l_orderhdr_data = []
    q_20_data = []
    queasy = l_order = l_orderhdr = l_artikel = htparam = bediener = l_lieferant = parameters = waehrung = None

    q_20 = t_l_order = t_l_orderhdr = t_l_artikel = None

    q_20_data, Q_20 = create_model_like(Queasy)
    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "art_bezeich":string, "jahrgang":int, "alkoholgrad":Decimal, "lief_einheit":Decimal})
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal enforce_rflag, show_price, qty_flag, qty_tol, higherprice_flag, disc_flag, crterm, price_decimal, lieferdatum, bestellart, comments, supplier, deptname, billdate, last_mdate, last_fbdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, t_amount, order_amt, exchg_rate, waehrung_wabkurz, fl_code, fl_code1, avail_param, fl_warn, avail_waehrung, ci_date, rcv_po, t_l_order_data, t_l_orderhdr_data, q_20_data, queasy, l_order, l_orderhdr, l_artikel, htparam, bediener, l_lieferant, parameters, waehrung
        nonlocal lief_nr, docu_nr, user_init


        nonlocal q_20, t_l_order, t_l_orderhdr, t_l_artikel
        nonlocal q_20_data, t_l_order_data, t_l_orderhdr_data, t_l_artikel_data

        return {"enforce_rflag": enforce_rflag, "show_price": show_price, "qty_flag": qty_flag, "qty_tol": qty_tol, "higherprice_flag": higherprice_flag, "disc_flag": disc_flag, "crterm": crterm, "price_decimal": price_decimal, "lieferdatum": lieferdatum, "bestellart": bestellart, "comments": comments, "supplier": supplier, "deptname": deptname, "billdate": billdate, "last_mdate": last_mdate, "last_fbdate": last_fbdate, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "t_amount": t_amount, "order_amt": order_amt, "exchg_rate": exchg_rate, "waehrung_wabkurz": waehrung_wabkurz, "fl_code": fl_code, "fl_code1": fl_code1, "avail_param": avail_param, "fl_warn": fl_warn, "avail_waehrung": avail_waehrung, "ci_date": ci_date, "rcv_po": rcv_po, "t-l-order": t_l_order_data, "t-l-orderhdr": t_l_orderhdr_data, "q-20": q_20_data}

    def cal_tamount():

        nonlocal enforce_rflag, show_price, qty_flag, qty_tol, higherprice_flag, disc_flag, crterm, price_decimal, lieferdatum, bestellart, comments, supplier, deptname, billdate, last_mdate, last_fbdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, t_amount, order_amt, exchg_rate, waehrung_wabkurz, fl_code, fl_code1, avail_param, fl_warn, avail_waehrung, ci_date, rcv_po, t_l_order_data, t_l_orderhdr_data, q_20_data, queasy, l_order, l_orderhdr, l_artikel, htparam, bediener, l_lieferant, parameters, waehrung
        nonlocal lief_nr, docu_nr, user_init


        nonlocal q_20, t_l_order, t_l_orderhdr, t_l_artikel
        nonlocal q_20_data, t_l_order_data, t_l_orderhdr_data, t_l_artikel_data


        t_amount =  to_decimal("0")
        order_amt =  to_decimal("0")

        l_order = get_cache (L_order, {"docu_nr": [(eq, docu_nr)],"pos": [(gt, 0)],"loeschflag": [(eq, 0)]})
        while None != l_order:
            order_amt =  to_decimal(order_amt) + to_decimal(l_order.warenwert)

            curr_recid = l_order._recid
            l_order = db_session.query(L_order).filter(
                     (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order._recid > curr_recid)).first()


    def get_currency():

        nonlocal enforce_rflag, show_price, qty_flag, qty_tol, higherprice_flag, disc_flag, crterm, price_decimal, lieferdatum, bestellart, comments, supplier, deptname, billdate, last_mdate, last_fbdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, t_amount, order_amt, exchg_rate, waehrung_wabkurz, fl_code, fl_code1, avail_param, fl_warn, avail_waehrung, ci_date, rcv_po, t_l_order_data, t_l_orderhdr_data, q_20_data, queasy, l_order, l_orderhdr, l_artikel, htparam, bediener, l_lieferant, parameters, waehrung
        nonlocal lief_nr, docu_nr, user_init


        nonlocal q_20, t_l_order, t_l_orderhdr, t_l_artikel
        nonlocal q_20_data, t_l_order_data, t_l_orderhdr_data, t_l_artikel_data

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, l_orderhdr.angebot_lief[2])]})

        if waehrung:
            waehrung_wabkurz = waehrung.wabkurz
            avail_waehrung = True
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr.docu_nr == (docu_nr).lower())).with_for_update().first()

    if l_orderhdr:
        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_data.append(t_l_orderhdr)

        buffer_copy(l_orderhdr, t_l_orderhdr)
        t_l_orderhdr.rec_id = l_orderhdr._recid

    htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
    enforce_rflag = htparam.flogical

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1010)],"paramgruppe": [(eq, 21)]})

    if htparam:
        qty_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1011)],"paramgruppe": [(eq, 21)]})

        if htparam:
            qty_tol = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 350)]})
    higherprice_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 349)]})

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    lieferdatum = l_orderhdr.lieferdatum
    bestellart = l_orderhdr.bestellart
    comments = l_orderhdr.lief_fax[2]
    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort

    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

    if parameters:
        deptname = parameters.vstring
        avail_param = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    if billdate == None or billdate > get_current_date():
        billdate = get_current_date()
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})

        if htparam.fdate != None:
            last_mdate = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate)) - timedelta(days=1)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

        if htparam.fdate != None:
            last_fbdate = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate)) - timedelta(days=1)

        if (billdate <= last_mdate) or (billdate <= last_fbdate):
            fl_warn = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})

        if htparam.fdate != None and billdate <= htparam.fdate:
            fl_code = 2

            return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    b_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    m_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    fb_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    m_closedate = htparam.fdate
    cal_tamount()
    get_currency()

    l_order = get_cache (L_order, {"docu_nr": [(eq, docu_nr)],"pos": [(gt, 0)],"loeschflag": [(eq, 0)]})
    while None != l_order:
        t_l_order = T_l_order()
        t_l_order_data.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})
        t_l_order.art_bezeich = l_artikel.bezeich
        t_l_order.jahrgang = l_artikel.jahrgang
        t_l_order.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)
        t_l_order.lief_einheit =  to_decimal(l_artikel.lief_einheit)

        curr_recid = l_order._recid
        l_order = db_session.query(L_order).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order._recid > curr_recid)).first()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 20)).order_by(Queasy._recid).all():
        q_20 = Q_20()
        q_20_data.append(q_20)

        buffer_copy(queasy, q_20)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1354)],"bezeichnung": [(ne, "not used")]})

    if htparam:
        rcv_po = htparam.flogical

    return generate_output()