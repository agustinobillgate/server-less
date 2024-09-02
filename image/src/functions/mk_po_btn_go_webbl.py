from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, L_order, L_artikel, Waehrung, Htparam

def mk_po_btn_go_webbl(t_l_orderhdr:[T_l_orderhdr], t_l_order:[T_l_order], docu_nr:str, lief_nr:int, billdate:date, create_new:bool, pr:str, globaldisc:decimal, currency_screen_value:str):
    fl_code = 0
    avail_hdrbuff = False
    new_docu_nr = ""
    l_orderhdr = l_order = l_artikel = waehrung = htparam = None

    t_l_orderhdr = t_l_order = hdrbuff = l_od = l_art1 = l_orderhdr1 = None

    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":str, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal, "disc_val":decimal, "disc2_val":decimal, "vat_val":decimal})

    Hdrbuff = L_orderhdr
    L_od = L_order
    L_art1 = L_artikel
    L_orderhdr1 = L_orderhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, avail_hdrbuff, new_docu_nr, l_orderhdr, l_order, l_artikel, waehrung, htparam
        nonlocal hdrbuff, l_od, l_art1, l_orderhdr1


        nonlocal t_l_orderhdr, t_l_order, hdrbuff, l_od, l_art1, l_orderhdr1
        nonlocal t_l_orderhdr_list, t_l_order_list
        return {"fl_code": fl_code, "avail_hdrbuff": avail_hdrbuff, "new_docu_nr": new_docu_nr}

    def new_po_number():

        nonlocal fl_code, avail_hdrbuff, new_docu_nr, l_orderhdr, l_order, l_artikel, waehrung, htparam
        nonlocal hdrbuff, l_od, l_art1, l_orderhdr1


        nonlocal t_l_orderhdr, t_l_order, hdrbuff, l_od, l_art1, l_orderhdr1
        nonlocal t_l_orderhdr_list, t_l_order_list

        s:str = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        L_orderhdr1 = L_orderhdr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 973)).first()

        if htparam.paramgruppe == 21 and htparam.flogical:
            mm = get_month(billdate)
            yy = get_year(billdate)
            s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99")

            for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                    (get_month(L_orderhdr1.bestelldatum) == mm) &  (get_year(L_orderhdr1.bestelldatum) == yy) &  (L_orderhdr1.betriebsnr <= 1) &  (L_orderhdr1.docu_nr.op("~")("P.*"))).all():
                i = to_int(substring(l_orderhdr1.docu_nr, 5, 5))
                i = i + 1
                new_docu_nr = s + to_string(i, "99999")

                return
            new_docu_nr = s + to_string(i, "99999")

            return
        s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                (L_orderhdr1.bestelldatum == billdate) &  (L_orderhdr1.betriebsnr <= 1) &  (L_orderhdr1.docu_nr.op("~")("P.*"))).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            new_docu_nr = s + to_string(i, "999")

            return
        new_docu_nr = s + to_string(i, "999")


    t_l_orderhdr = query(t_l_orderhdr_list, first=True)

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == t_L_orderhdr.rec_id)).first()
    buffer_copy(t_l_orderhdr, l_orderhdr)

    waehrung = db_session.query(Waehrung).filter(
            (func.lower(Waehrung.wabkurz) == (currency_screen_value).lower())).first()

    if waehrung:
        l_orderhdr.angebot_lief[2] = waehrungsnr

    for t_l_order in query(t_l_order_list, filters=(lambda t_l_order :t_l_order.pos > 0 and t_l_order.(docu_nr).lower().lower()  == (docu_nr).lower()  and t_l_order.betriebsnr >= 98)):

        if t_l_order.betriebsnr == 99:
            t_l_order.geliefert = 0
        t_l_order.betriebsnr = 2

    t_l_order = query(t_l_order_list, filters=(lambda t_l_order :t_l_order.pos > 0 and t_l_order.(docu_nr).lower().lower()  == (docu_nr).lower()  and t_l_order.betriebsnr == 2), first=True)

    if not t_l_order:
        fl_code = 1

        hdrbuff = db_session.query(Hdrbuff).filter(
                (Hdrbuff.docu_nr == l_orderhdr.docu_nr) &  (Hdrbuff._recid != l_orderhdr._recid)).first()

        if hdrbuff:
            new_po_number()
            l_orderhdr.docu_nr = new_docu_nr


            avail_hdrbuff = True

            return generate_output()

    t_l_order = query(t_l_order_list, filters=(lambda t_l_order :t_l_order.(docu_nr).lower().lower()  == (docu_nr).lower()  and t_l_order.pos > 0 and t_l_order.einzelpreis == 0 and t_l_order.betriebsnr == 2), first=True)

    if t_l_order:
        fl_code = 2

        return generate_output()

    for t_l_order in query(t_l_order_list, filters=(lambda t_l_order :t_l_order.pos > 0)):

        l_art1 = db_session.query(L_art1).filter(
                (L_art1.artnr == t_l_order.artnr)).first()

        l_order = db_session.query(L_order).filter(
                (L_order._recid == t_L_order.rec_id)).first()

        if l_order:
            l_order.quality = to_string(t_l_order.disc, "99.99 ") +\
                    to_string(t_l_order.vat, "99.99") + to_string(t_l_order.disc2, " 99.99") +\
                    to_string(t_l_order.disc_val, " >,>>>,>>>,>>9.999") + to_string(t_l_order.disc2_val, " >,>>>,>>>,>>9.999") +\
                    to_string(t_l_order.vat_val, " >,>>>,>>>,>>9.999")
            l_order.warenwert = t_l_order.warenwert
            l_order.einzelpreis = t_l_order.einzelpreis
            l_order.lief_nr = lief_nr
            l_order.betriebsnr = 0


            l_order.geliefert = t_l_order.geliefert

            if not l_order.flag:
                l_order.warenwert = l_order.warenwert * l_art1.lief_einheit

            l_order = db_session.query(L_order).first()
        else:
            l_order = L_order()
            db_session.add(l_order)

            buffer_copy(t_l_order, l_order)

            if t_l_order.disc != 0 or t_l_order.disc2 != 0 or t_l_order.vat != 0 or t_l_order.disc_val != 0 or t_l_order.disc2_val != 0 or t_l_order.vat_val != 0:
                l_order.quality = to_string(t_l_order.disc, "99.99 ") +\
                    to_string(t_l_order.vat, "99.99") + to_string(t_l_order.disc2, " 99.99") +\
                    to_string(t_l_order.disc_val, " >,>>>,>>>,>>9.999") + to_string(t_l_order.disc2_val, " >,>>>,>>>,>>9.999") +\
                    to_string(t_l_order.vat_val, " >,>>>,>>>,>>9.999")


            l_order.betriebsnr = 0

    if create_new:
        l_od = L_od()
        db_session.add(l_od)

        l_od.docu_nr = docu_nr
        l_od.pos = 0
        l_od.bestelldatum = l_orderhdr.bestelldatum
        l_od.lief_nr = lief_nr
        l_od.op_art = 2
        l_od.lief_fax[0] = pr
        l_od.betriebsnr = 2

    l_od = db_session.query(L_od).filter(
            (func.lower(L_od.(docu_nr).lower()) == (docu_nr).lower()) &  (L_od.pos == 0) &  (L_od.op_art == 2)).first()

    if l_od:
        l_od.warenwert = globaldisc
        l_od.lief_nr = lief_nr
        l_od.lief_fax[0] = pr

        l_od = db_session.query(L_od).first()

    return generate_output()