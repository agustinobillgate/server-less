from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_ophdr, Htparam, L_lieferant, L_lager, Bediener

def prepare_s_stockinsbl(l_recid:int, rcvdate:date):
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
    lief_bezeich = ""
    lager_bezeich = ""
    err_code = 0
    fl_code1 = 0
    fl_code2 = 0
    l_rcv_lscheinnr = ""
    l_out_stornogrund = ""
    avail_l_out = False
    t_bediener_list = []
    l_op = l_ophdr = htparam = l_lieferant = l_lager = bediener = None

    t_bediener = l_rcv = l_out = None

    t_bediener_list, T_bediener = create_model("T_bediener", {"username":str, "nr":int})

    L_rcv = L_op
    L_out = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rcv_type, f_endkum, b_endkum, m_endkum, lief_nr, curr_lager, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, lscheinnr, lief_bezeich, lager_bezeich, err_code, fl_code1, fl_code2, l_rcv_lscheinnr, l_out_stornogrund, avail_l_out, t_bediener_list, l_op, l_ophdr, htparam, l_lieferant, l_lager, bediener
        nonlocal l_rcv, l_out


        nonlocal t_bediener, l_rcv, l_out
        nonlocal t_bediener_list
        return {"rcv_type": rcv_type, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "lief_nr": lief_nr, "curr_lager": curr_lager, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "last_mdate": last_mdate, "last_fbdate": last_fbdate, "lscheinnr": lscheinnr, "lief_bezeich": lief_bezeich, "lager_bezeich": lager_bezeich, "err_code": err_code, "fl_code1": fl_code1, "fl_code2": fl_code2, "l_rcv_lscheinnr": l_rcv_lscheinnr, "l_out_stornogrund": l_out_stornogrund, "avail_l_out": avail_l_out, "t-bediener": t_bediener_list}

    l_rcv = db_session.query(L_rcv).filter(
            (L_rcv._recid == l_recid)).first()
    rcv_type = l_rcv.herkunftflag

    if rcv_type == 2:

        l_out = db_session.query(L_out).filter(
                (L_out.lief_nr == l_rcv.lief_nr) &  (L_out.datum == l_rcv.datum) &  (L_out.lager_nr == l_rcv.lager_nr) &  (L_out.artnr == l_rcv.artnr) &  (L_out.anzahl == l_rcv.anzahl) &  (L_out.einzelpreis == l_rcv.einzelpreis) &  (L_out.warenwert == l_rcv.warenwert) &  (L_out.op_art == 3) &  (L_out.herkunftflag == 2) &  (L_out.docu_nr == l_rcv.docu_nr) &  (L_out.lscheinnr == l_rcv.lscheinnr)).first()

        if not l_out:
            err_code = 1

            return generate_output()
        else:
            l_out_stornogrund = l_out.stornogrund
            avail_l_out = True

    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr.lscheinnr == l_rcv.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.datum == l_rcv.datum)).first()

    if not l_ophdr:
        err_code = 2
        l_rcv_lscheinnr = l_rcv.lscheinnr

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
    billdate = rcvdate

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
            fl_code1 = 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 269)).first()

        if htparam.fdate != None and billdate <= htparam.fdate:
            fl_code2 = 1
    lief_nr = l_rcv.lief_nr
    lscheinnr = l_rcv.lscheinnr
    billdate = l_rcv.datum
    curr_lager = l_rcv.lager_nr

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == curr_lager)).first()
    lief_bezeich = l_lieferant.firma
    lager_bezeich = l_lager.bezeich

    for bediener in db_session.query(Bediener).all():
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        t_bediener.username = bediener.username
        t_bediener.nr = bediener.nr

    return generate_output()