#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.s_stockins_create_apbl import s_stockins_create_apbl
from models import L_op, L_artikel, L_bestand, L_lieferant, L_liefumsatz, L_pprice, Htparam

op_list_list, Op_list = create_model_like(L_op, {"a_bezeich":string})

def s_stockins_btn_gobl(curr_pos:int, s_artnr:int, price:Decimal, t_amount:Decimal, curr_lager:int, op_list_list:[Op_list], pvilanguage:int, l_out_stornogrund:string, lief_nr:int, billdate:date, fb_closedate:date, m_closedate:date, m_endkum:int, f_endkum:int, b_endkum:int, avail_l_out:bool, lscheinnr:string, rcv_type:int, qty:Decimal, user_init:string):

    prepare_cache ([L_op, L_artikel, L_bestand, L_liefumsatz, L_pprice, Htparam])

    created = False
    msg_str = ""
    lvcarea:string = "s-stockins"
    l_op = l_artikel = l_bestand = l_lieferant = l_liefumsatz = l_pprice = htparam = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, msg_str, lvcarea, l_op, l_artikel, l_bestand, l_lieferant, l_liefumsatz, l_pprice, htparam
        nonlocal curr_pos, s_artnr, price, t_amount, curr_lager, pvilanguage, l_out_stornogrund, lief_nr, billdate, fb_closedate, m_closedate, m_endkum, f_endkum, b_endkum, avail_l_out, lscheinnr, rcv_type, qty, user_init


        nonlocal op_list

        return {"curr_pos": curr_pos, "s_artnr": s_artnr, "price": price, "t_amount": t_amount, "curr_lager": curr_lager, "created": created, "msg_str": msg_str}

    def create_l_op():

        nonlocal created, msg_str, lvcarea, l_op, l_artikel, l_bestand, l_lieferant, l_liefumsatz, l_pprice, htparam
        nonlocal curr_pos, s_artnr, price, t_amount, curr_lager, pvilanguage, l_out_stornogrund, lief_nr, billdate, fb_closedate, m_closedate, m_endkum, f_endkum, b_endkum, avail_l_out, lscheinnr, rcv_type, qty, user_init


        nonlocal op_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        wert =  to_decimal(round (wert , 2))

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)


            pass
            tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) -\
                    l_bestand.anz_ausgang
            tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) -\
                    l_bestand.wert_ausgang

            if (tot_anz != 0) and (rcv_type != 2):
                avrg_price =  to_decimal(tot_wert) / to_decimal(tot_anz)
                pass
                l_artikel.vk_preis =  to_decimal(avrg_price)
                pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, op_list.lager_nr)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = op_list.lager_nr
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)


            pass

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

        if l_lieferant:

            l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, lief_nr)],"datum": [(eq, billdate)]})

            if not l_liefumsatz:
                l_liefumsatz = L_liefumsatz()
                db_session.add(l_liefumsatz)

                l_liefumsatz.datum = billdate
                l_liefumsatz.lief_nr = lief_nr


            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(wert)
            pass
        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        l_op.pos = curr_pos
        l_op.lief_nr = lief_nr


        pass
        create_purchase_book(s_artnr, price, anzahl, billdate, lief_nr)

        if (l_artikel.ek_aktuell != price) and price != 0:
            pass
            l_artikel.ek_letzter =  to_decimal(l_artikel.ek_aktuell)
            l_artikel.ek_aktuell =  to_decimal(price)


            pass

        return
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Incoming record for article ", lvcarea, "") + to_string(s_artnr, "9999999") + " could not be created!!!"


    def create_l_op1():

        nonlocal created, msg_str, lvcarea, l_op, l_artikel, l_bestand, l_lieferant, l_liefumsatz, l_pprice, htparam
        nonlocal curr_pos, s_artnr, price, t_amount, curr_lager, pvilanguage, l_out_stornogrund, lief_nr, billdate, fb_closedate, m_closedate, m_endkum, f_endkum, b_endkum, avail_l_out, lscheinnr, rcv_type, qty, user_init


        nonlocal op_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        l_art = None
        L_art =  create_buffer("L_art",L_artikel)
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        wert = to_decimal(round(wert , 2))


        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        l_op.pos = op_list.lager_nr
        l_op.lief_nr = lief_nr
        l_op.op_art = 3
        l_op.stornogrund = l_out_stornogrund


        pass

        l_art = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

        if ((l_art.endkum == f_endkum or l_art.endkum == b_endkum) and billdate <= fb_closedate) or (l_art.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, op_list.lager_nr)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = op_list.lager_nr
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)


            pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = 0
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)


            pass


    def create_purchase_book(s_artnr:int, price:Decimal, qty:Decimal, datum:date, lief_nr:int):

        nonlocal msg_str, lvcarea, l_op, l_artikel, l_bestand, l_lieferant, l_liefumsatz, l_pprice, htparam
        nonlocal curr_pos, t_amount, curr_lager, pvilanguage, l_out_stornogrund, billdate, fb_closedate, m_closedate, m_endkum, f_endkum, b_endkum, avail_l_out, lscheinnr, rcv_type, user_init


        nonlocal op_list

        max_anz:int = 0
        curr_anz:int = 0
        created:bool = False
        i:int = 0
        l_art = None
        l_price1 = None
        L_art =  create_buffer("L_art",L_artikel)
        L_price1 =  create_buffer("L_price1",L_pprice)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 225)]})
        max_anz = htparam.finteger

        if max_anz == 0:
            max_anz = 1

        l_art = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
        curr_anz = l_art.lieferfrist

        if curr_anz >= max_anz:

            l_price1 = get_cache (L_pprice, {"artnr": [(eq, s_artnr)],"counter": [(eq, 1)]})

            if l_price1:
                l_price1.docu_nr = lscheinnr
                l_price1.artnr = s_artnr
                l_price1.anzahl =  to_decimal(qty)
                l_price1.einzelpreis =  to_decimal(price)
                l_price1.warenwert =  to_decimal(qty) * to_decimal(price)
                l_price1.bestelldatum = datum
                l_price1.lief_nr = lief_nr
                l_price1.counter = 0
                created = True
            for i in range(2,curr_anz + 1) :

                l_pprice = get_cache (L_pprice, {"artnr": [(eq, s_artnr)],"counter": [(eq, i)]})

                if l_pprice:
                    pass
                    l_pprice.counter = l_pprice.counter - 1
                    pass

            if created:
                l_price1.counter = curr_anz
                pass

        if not created:
            l_pprice = L_pprice()
            db_session.add(l_pprice)

            l_pprice.docu_nr = lscheinnr
            l_pprice.artnr = s_artnr
            l_pprice.anzahl =  to_decimal(qty)
            l_pprice.einzelpreis =  to_decimal(price)
            l_pprice.warenwert =  to_decimal(qty) * to_decimal(price)
            l_pprice.bestelldatum = datum
            l_pprice.lief_nr = lief_nr
            l_pprice.counter = curr_anz + 1
            pass
            pass
            l_art.lieferfrist = curr_anz + 1
            pass


    for op_list in query(op_list_list):
        op_list.docu_nr = lscheinnr
        op_list.lscheinnr = lscheinnr
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        t_amount =  to_decimal(t_amount) + to_decimal(op_list.warenwert)
        curr_lager = op_list.lager_nr

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
        create_l_op()

        if rcv_type == 2 and avail_l_out:
            create_l_op1()
        created = True

    if lief_nr != 0 and t_amount != 0:
        get_output(s_stockins_create_apbl(lief_nr, lscheinnr, billdate, t_amount, user_init))

    return generate_output()