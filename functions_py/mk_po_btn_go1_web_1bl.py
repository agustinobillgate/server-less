#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, L_order, L_artikel, Waehrung, Queasy, Htparam

t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":string, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "disc_val":Decimal, "disc2_val":Decimal, "vat_val":Decimal, "addvat_no":int, "addvat_value":Decimal})

def mk_po_btn_go1_web_1bl(t_l_orderhdr_data:[T_l_orderhdr], t_l_order_data:[T_l_order], docu_nr:string, lief_nr:int, billdate:date, create_new:bool, pr:string, globaldisc:Decimal, currency_screen_value:string, zeroprice_flag:bool):

    prepare_cache ([L_orderhdr, L_order, L_artikel, Waehrung, Queasy, Htparam])

    fl_code = 0
    avail_hdrbuff = False
    new_docu_nr = ""
    l_orderhdr = l_order = l_artikel = waehrung = queasy = htparam = None

    t_l_orderhdr = t_l_order = hdrbuff = l_od = l_art1 = None

    Hdrbuff = create_buffer("Hdrbuff",L_orderhdr)
    L_od = create_buffer("L_od",L_order)
    L_art1 = create_buffer("L_art1",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, avail_hdrbuff, new_docu_nr, l_orderhdr, l_order, l_artikel, waehrung, queasy, htparam
        nonlocal docu_nr, lief_nr, billdate, create_new, pr, globaldisc, currency_screen_value, zeroprice_flag
        nonlocal hdrbuff, l_od, l_art1


        nonlocal t_l_orderhdr, t_l_order, hdrbuff, l_od, l_art1

        return {"fl_code": fl_code, "avail_hdrbuff": avail_hdrbuff, "new_docu_nr": new_docu_nr}

    def new_po_number():

        nonlocal fl_code, avail_hdrbuff, new_docu_nr, l_orderhdr, l_order, l_artikel, waehrung, queasy, htparam
        nonlocal docu_nr, lief_nr, billdate, create_new, pr, globaldisc, currency_screen_value, zeroprice_flag
        nonlocal hdrbuff, l_od, l_art1


        nonlocal t_l_orderhdr, t_l_order, hdrbuff, l_od, l_art1

        l_orderhdr1 = None
        s:string = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        L_orderhdr1 =  create_buffer("L_orderhdr1",L_orderhdr)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 973)]})

        if htparam.paramgruppe == 21 and htparam.flogical:
            mm = get_month(billdate)
            yy = get_year(billdate)
            s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99")

            for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                     (get_month(L_orderhdr1.bestelldatum) == mm) & (get_year(L_orderhdr1.bestelldatum) == yy) & (L_orderhdr1.betriebsnr <= 1) & (matches(L_orderhdr1.docu_nr,"P*"))).order_by(L_orderhdr1.docu_nr.desc()).all():
                i = to_int(substring(l_orderhdr1.docu_nr, 5, 5))
                i = i + 1
                new_docu_nr = s + to_string(i, "99999")

                return
            new_docu_nr = s + to_string(i, "99999")

            return
        s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                 (L_orderhdr1.bestelldatum == billdate) & (L_orderhdr1.betriebsnr <= 1) & (matches(L_orderhdr1.docu_nr,"P*"))).order_by(L_orderhdr1.docu_nr.desc()).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            new_docu_nr = s + to_string(i, "999")

            return
        new_docu_nr = s + to_string(i, "999")

    # Rd, 17-July-25
    # t_l_orderhdr = query(t_l_orderhdr_data, first=True)
    # l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, t_l_orderhdr.rec_id)]})
    if not t_l_orderhdr_data:
        return generate_output() 
    
    t_l_orderhdr = t_l_orderhdr_data[0]
    l_orderhdr = db_session.query(L_orderhdr)\
        .filter(L_orderhdr._recid == t_l_orderhdr.rec_id)\
        .first()
    if not t_l_orderhdr:
        return generate_output()

    l_orderhdr = db_session.query(L_orderhdr)\
        .filter(L_orderhdr._recid == t_l_orderhdr.rec_id)\
        .first()

    if not l_orderhdr:
        return generate_output()
    
    buffer_copy(t_l_orderhdr, l_orderhdr)

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, currency_screen_value)]})

    if waehrung:
        l_orderhdr.angebot_lief[2] = waehrung.waehrungsnr

    for t_l_order in query(t_l_order_data, filters=(lambda t_l_order: t_l_order.pos > 0 and t_l_order.docu_nr.lower()  == (docu_nr).lower()  and t_l_order.betriebsnr >= 98)):

        if t_l_order.betriebsnr == 99:
            t_l_order.geliefert =  to_decimal("0")
        t_l_order.betriebsnr = 2

    t_l_order = query(t_l_order_data, filters=(lambda t_l_order: t_l_order.pos > 0 and t_l_order.docu_nr.lower()  == (docu_nr).lower()  and t_l_order.betriebsnr == 2), first=True)

    if not t_l_order:
        fl_code = 1

        hdrbuff = get_cache (L_orderhdr, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"_recid": [(ne, l_orderhdr._recid)]})

        if hdrbuff:
            new_po_number()
            l_orderhdr.docu_nr = new_docu_nr


            avail_hdrbuff = True

            return generate_output()

    t_l_order = query(t_l_order_data, filters=(lambda t_l_order: t_l_order.docu_nr.lower()  == (docu_nr).lower()  and t_l_order.pos > 0 and t_l_order.einzelpreis == 0 and t_l_order.betriebsnr == 2), first=True)

    if t_l_order:
        fl_code = 2

        if not zeroprice_flag:

            return generate_output()
        else:

            hdrbuff = get_cache (L_orderhdr, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"_recid": [(ne, l_orderhdr._recid)]})

            if hdrbuff:
                new_po_number()
                l_orderhdr.docu_nr = new_docu_nr


                avail_hdrbuff = True

                return generate_output()

    for t_l_order in query(t_l_order_data, filters=(lambda t_l_order: t_l_order.pos > 0)):

        l_art1 = get_cache (L_artikel, {"artnr": [(eq, t_l_order.artnr)]})

        l_order = get_cache (L_order, {"_recid": [(eq, t_l_order.rec_id)]})

        if l_order:
            l_order.quality = to_string(t_l_order.disc, "99.99 ") +\
                    to_string(t_l_order.vat, "99.99") + to_string(t_l_order.disc2, " 99.99") +\
                    to_string(t_l_order.disc_val, " >,>>>,>>>,>>9.999") + to_string(t_l_order.disc2_val, " >,>>>,>>>,>>9.999") +\
                    to_string(t_l_order.vat_val, " >,>>>,>>>,>>9.999")
            l_order.warenwert =  to_decimal(t_l_order.warenwert)
            l_order.einzelpreis =  to_decimal(t_l_order.einzelpreis)
            l_order.lief_nr = lief_nr
            l_order.betriebsnr = 0


            l_order.geliefert =  to_decimal(t_l_order.geliefert)

            if not l_order.flag:
                l_order.warenwert =  to_decimal(l_order.warenwert) * to_decimal(l_art1.lief_einheit)

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, t_l_order.docu_nr)],"number1": [(eq, t_l_order.artnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 304
                queasy.char1 = t_l_order.docu_nr
                queasy.number1 = t_l_order.artnr
                queasy.number2 = t_l_order.addvat_no
                queasy.deci1 =  to_decimal(t_l_order.addvat_value)


                pass
            else:
                pass
                queasy.char1 = t_l_order.docu_nr
                queasy.number1 = t_l_order.artnr
                queasy.number2 = t_l_order.addvat_no
                queasy.deci1 =  to_decimal(t_l_order.addvat_value)


                pass
                pass
            pass
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

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, t_l_order.docu_nr)],"number1": [(eq, t_l_order.artnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 304
                queasy.char1 = t_l_order.docu_nr
                queasy.number1 = t_l_order.artnr
                queasy.number2 = t_l_order.addvat_no
                queasy.deci1 =  to_decimal(t_l_order.addvat_value)


                pass

    if create_new:
        l_od = L_order()
        db_session.add(l_od)

        l_od.docu_nr = docu_nr
        l_od.pos = 0
        l_od.bestelldatum = l_orderhdr.bestelldatum
        l_od.lief_nr = lief_nr
        l_od.op_art = 2
        l_od.lief_fax[0] = pr
        l_od.betriebsnr = 2

    l_od = get_cache (L_order, {"docu_nr": [(eq, docu_nr)],"pos": [(eq, 0)],"op_art": [(eq, 2)]})

    if l_od:
        l_od.warenwert =  to_decimal(globaldisc)
        l_od.lief_nr = lief_nr
        l_od.lief_fax[0] = pr


        pass

    return generate_output()