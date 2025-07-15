from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, L_order, Htparam

t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

def mk_po_btn_go1bl(t_l_orderhdr_list:[T_l_orderhdr], docu_nr:str, recid_l_orderhdr:int, billdate:date):
    fl_code = 0
    avail_hdrbuff = False
    new_docu_nr = ""
    l_orderhdr = l_order = htparam = None

    t_l_orderhdr = hdrbuff = None

    Hdrbuff = create_buffer("Hdrbuff",L_orderhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, avail_hdrbuff, new_docu_nr, l_orderhdr, l_order, htparam
        nonlocal docu_nr, recid_l_orderhdr, billdate
        nonlocal hdrbuff


        nonlocal t_l_orderhdr, hdrbuff
        nonlocal t_l_orderhdr_list
        return {"fl_code": fl_code, "avail_hdrbuff": avail_hdrbuff, "new_docu_nr": new_docu_nr}

    def new_po_number():

        nonlocal fl_code, avail_hdrbuff, new_docu_nr, l_orderhdr, l_order, htparam
        nonlocal docu_nr, recid_l_orderhdr, billdate
        nonlocal hdrbuff


        nonlocal t_l_orderhdr, hdrbuff
        nonlocal t_l_orderhdr_list

        l_orderhdr1 = None
        s:str = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        L_orderhdr1 =  create_buffer("L_orderhdr1",L_orderhdr)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 973)).first()

        if htparam.paramgruppe == 21 and htparam.flogical:
            mm = get_month(billdate)
            yy = get_year(billdate)
            s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99")

            for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                     (get_month(L_orderhdr1.bestelldatum) == mm) & (get_year(L_orderhdr1.bestelldatum) == yy) & (L_orderhdr1.betriebsnr <= 1) & (func.lower(L_orderhdr1.docu_nr).op("~")(("P*".lower().replace("*",".*"))))).order_by(L_orderhdr1.docu_nr.desc()).all():
                i = to_int(substring(l_orderhdr1.docu_nr, 5, 5))
                i = i + 1
                new_docu_nr = s + to_string(i, "99999")

                return
            new_docu_nr = s + to_string(i, "99999")

            return
        s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                 (L_orderhdr1.bestelldatum == billdate) & (L_orderhdr1.betriebsnr <= 1) & (func.lower(L_orderhdr1.docu_nr).op("~")(("P*".lower().replace("*",".*"))))).order_by(L_orderhdr1.docu_nr.desc()).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            new_docu_nr = s + to_string(i, "999")

            return
        new_docu_nr = s + to_string(i, "999")


    t_l_orderhdr = query(t_l_orderhdr_list, first=True)

    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr._recid == t_l_orderhdr.rec_id)).first()
    buffer_copy(t_l_orderhdr, l_orderhdr)

    l_order = db_session.query(L_order).filter(
             (L_order.pos > 0) & (func.lower(L_order.docu_nr) == (docu_nr).lower()) & (L_order.betriebsnr == 2)).first()

    if not l_order:
        fl_code = 1

        hdrbuff = db_session.query(Hdrbuff).filter(
                 (Hdrbuff.docu_nr == l_orderhdr.docu_nr) & (Hdrbuff._recid != l_orderhdr._recid)).first()

        if hdrbuff:
            new_po_number()
            l_orderhdr.docu_nr = new_docu_nr


            avail_hdrbuff = True

        return generate_output()

    l_order = db_session.query(L_order).filter(
             (func.lower(L_order.docu_nr) == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.einzelpreis == 0) & (L_order.betriebsnr == 2)).first()

    if l_order:
        fl_code = 2

    return generate_output()