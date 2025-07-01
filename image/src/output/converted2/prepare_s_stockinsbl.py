#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_ophdr, Htparam, L_lieferant, L_lager, Bediener

def prepare_s_stockinsbl(l_recid:int, rcvdate:date):

    prepare_cache ([L_op, Htparam, L_lieferant, L_lager, Bediener])

    rcv_type = 0
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    lief_nr = 0
    curr_lager = 0
    billdate = None
    fb_closedate = None
    m_closedate = None
    last_mdate = None
    last_fbdate = None
    lscheinnr = ""
    lief_bezeich = "Supplier Name"
    lager_bezeich = "Store Name"
    err_code = 0
    fl_code1 = 0
    fl_code2 = 0
    l_rcv_lscheinnr = ""
    l_out_stornogrund = ""
    avail_l_out = False
    t_bediener_list = []
    l_op = l_ophdr = htparam = l_lieferant = l_lager = bediener = None

    t_bediener = l_rcv = l_out = None

    t_bediener_list, T_bediener = create_model("T_bediener", {"username":string, "nr":int})

    L_rcv = create_buffer("L_rcv",L_op)
    L_out = create_buffer("L_out",L_op)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rcv_type, f_endkum, b_endkum, m_endkum, lief_nr, curr_lager, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, lscheinnr, lief_bezeich, lager_bezeich, err_code, fl_code1, fl_code2, l_rcv_lscheinnr, l_out_stornogrund, avail_l_out, t_bediener_list, l_op, l_ophdr, htparam, l_lieferant, l_lager, bediener
        nonlocal l_recid, rcvdate
        nonlocal l_rcv, l_out


        nonlocal t_bediener, l_rcv, l_out
        nonlocal t_bediener_list

        return {"rcv_type": rcv_type, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "lief_nr": lief_nr, "curr_lager": curr_lager, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "last_mdate": last_mdate, "last_fbdate": last_fbdate, "lscheinnr": lscheinnr, "lief_bezeich": lief_bezeich, "lager_bezeich": lager_bezeich, "err_code": err_code, "fl_code1": fl_code1, "fl_code2": fl_code2, "l_rcv_lscheinnr": l_rcv_lscheinnr, "l_out_stornogrund": l_out_stornogrund, "avail_l_out": avail_l_out, "t-bediener": t_bediener_list}

    l_rcv = get_cache (L_op, {"_recid": [(eq, l_recid)]})
    rcv_type = l_rcv.herkunftflag

    if rcv_type == 2:

        l_out = get_cache (L_op, {"lief_nr": [(eq, l_rcv.lief_nr)],"datum": [(eq, l_rcv.datum)],"lager_nr": [(eq, l_rcv.lager_nr)],"artnr": [(eq, l_rcv.artnr)],"anzahl": [(eq, l_rcv.anzahl)],"einzelpreis": [(eq, l_rcv.einzelpreis)],"warenwert": [(eq, l_rcv.warenwert)],"op_art": [(eq, 3)],"herkunftflag": [(eq, 2)],"docu_nr": [(eq, l_rcv.docu_nr)],"lscheinnr": [(eq, l_rcv.lscheinnr)]})

        if not l_out:
            err_code = 1

            return generate_output()
        else:
            l_out_stornogrund = l_out.stornogrund
            avail_l_out = True

    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, l_rcv.lscheinnr)],"op_typ": [(eq, "sti")],"datum": [(eq, l_rcv.datum)]})

    if not l_ophdr:
        err_code = 2
        l_rcv_lscheinnr = l_rcv.lscheinnr

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    b_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    m_endkum = htparam.finteger
    billdate = rcvdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    fb_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    m_closedate = htparam.fdate

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
    lief_nr = l_rcv.lief_nr
    lscheinnr = l_rcv.lscheinnr
    billdate = l_rcv.datum
    curr_lager = l_rcv.lager_nr

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})
    lief_bezeich = l_lieferant.firma
    lager_bezeich = l_lager.bezeich

    for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        t_bediener.username = bediener.username
        t_bediener.nr = bediener.nr

    return generate_output()