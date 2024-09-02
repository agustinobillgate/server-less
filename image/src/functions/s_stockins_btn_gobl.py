from functions.additional_functions import *
import decimal
from datetime import date
from functions.s_stockins_create_apbl import s_stockins_create_apbl
from models import L_op, L_artikel, L_bestand, L_lieferant, L_liefumsatz, L_pprice, Htparam

def s_stockins_btn_gobl(curr_pos:int, s_artnr:int, price:decimal, t_amount:decimal, curr_lager:int, op_list:[Op_list], pvilanguage:int, l_out_stornogrund:str, lief_nr:int, billdate:date, fb_closedate:date, m_closedate:date, m_endkum:int, f_endkum:int, b_endkum:int, avail_l_out:bool, lscheinnr:str, rcv_type:int, qty:decimal, user_init:str):
    created = False
    msg_str = ""
    lvcarea:str = "s_stockins"
    l_op = l_artikel = l_bestand = l_lieferant = l_liefumsatz = l_pprice = htparam = None

    op_list = l_art = l_price1 = None

    op_list_list, Op_list = create_model_like(L_op, {"a_bezeich":str})

    L_art = L_artikel
    L_price1 = L_pprice

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, msg_str, lvcarea, l_op, l_artikel, l_bestand, l_lieferant, l_liefumsatz, l_pprice, htparam
        nonlocal l_art, l_price1


        nonlocal op_list, l_art, l_price1
        nonlocal op_list_list
        return {"created": created, "msg_str": msg_str}

    def create_l_op():

        nonlocal created, msg_str, lvcarea, l_op, l_artikel, l_bestand, l_lieferant, l_liefumsatz, l_pprice, htparam
        nonlocal l_art, l_price1


        nonlocal op_list, l_art, l_price1
        nonlocal op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0
        anzahl = qty
        wert = qty * price
        wert = round (wert, 2)

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = db_session.query(L_bestand).filter(
                            (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert

            l_bestand = db_session.query(L_bestand).first()
            tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang -\
                    l_bestand.anz_ausgang
            tot_wert = l_bestand.val_anf_best + l_bestand.wert_eingang -\
                    l_bestand.wert_ausgang

            if (tot_anz != 0) and (rcv_type != 2):
                avrg_price = tot_wert / tot_anz

                l_artikel = db_session.query(L_artikel).first()
                l_artikel.vk_preis = avrg_price

                l_artikel = db_session.query(L_artikel).first()

            l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.lager_nr == op_list.lager_nr) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = op_list.lager_nr
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert

            l_bestand = db_session.query(L_bestand).first()

        l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == lief_nr)).first()

        if l_lieferant:

            l_liefumsatz = db_session.query(L_liefumsatz).filter(
                        (L_liefumsatz.lief_nr == lief_nr) &  (L_liefumsatz.datum == billdate)).first()

            if not l_liefumsatz:
                l_liefumsatz = L_liefumsatz()
                db_session.add(l_liefumsatz)

                l_liefumsatz.datum = billdate
                l_liefumsatz.lief_nr = lief_nr


            l_liefumsatz.gesamtumsatz = l_liefumsatz.gesamtumsatz + wert

            l_liefumsatz = db_session.query(L_liefumsatz).first()
        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        l_op.pos = curr_pos
        l_op.lief_nr = lief_nr

        l_op = db_session.query(L_op).first()
        create_purchase_book(s_artnr, price, anzahl, billdate, lief_nr)

        if (l_artikel.ek_aktuell != price) and price != 0:

            l_artikel = db_session.query(L_artikel).first()
            l_artikel.ek_letzter = l_artikel.ek_aktuell
            l_artikel.ek_aktuell = price

            l_artikel = db_session.query(L_artikel).first()

        return

        msg_str = msg_str + chr(2) + translateExtended ("Incoming record for article ", lvcarea, "") + to_string(s_artnr, "9999999") + " could not be created!!!"

    def create_l_op1():

        nonlocal created, msg_str, lvcarea, l_op, l_artikel, l_bestand, l_lieferant, l_liefumsatz, l_pprice, htparam
        nonlocal l_art, l_price1


        nonlocal op_list, l_art, l_price1
        nonlocal op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0
        L_art = L_artikel
        anzahl = qty
        wert = qty * price
        wert = round(wert, 2)


        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        l_op.pos = op_list.lager_nr
        l_op.lief_nr = lief_nr
        l_op.op_art = 3
        l_op.stornogrund = l_out_stornogrund

        l_op = db_session.query(L_op).first()

        l_art = db_session.query(L_art).filter(
                (L_art.artnr == s_artnr)).first()

        if ((l_art.endkum == f_endkum or l_art.endkum == b_endkum) and billdate <= fb_closedate) or (l_art.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == op_list.lager_nr) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = op_list.lager_nr
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

            l_bestand = db_session.query(L_bestand).first()

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = 0
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

            l_bestand = db_session.query(L_bestand).first()

    def create_purchase_book(s_artnr:int, price:decimal, qty:decimal, datum:date, lief_nr:int):

        nonlocal created, msg_str, lvcarea, l_op, l_artikel, l_bestand, l_lieferant, l_liefumsatz, l_pprice, htparam
        nonlocal l_art, l_price1


        nonlocal op_list, l_art, l_price1
        nonlocal op_list_list

        max_anz:int = 0
        curr_anz:int = 0
        created:bool = False
        i:int = 0
        L_art = L_artikel
        L_price1 = L_pprice

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 225)).first()
        max_anz = htparam.finteger

        if max_anz == 0:
            max_anz = 1

        l_art = db_session.query(L_art).filter(
                (L_art.artnr == s_artnr)).first()
        curr_anz = l_art.lieferfrist

        if curr_anz >= max_anz:

            l_price1 = db_session.query(L_price1).filter(
                    (L_price1.artnr == s_artnr) &  (L_price1.counter == 1)).first()

            if l_price1:
                l_price1.docu_nr = lscheinnr
                l_price1.artnr = s_artnr
                l_price1.anzahl = qty
                l_price1.einzelpreis = price
                l_price1.warenwert = qty * price
                l_price1.bestelldatum = datum
                l_price1.lief_nr = lief_nr
                l_price1.counter = 0
                created = True
            for i in range(2,curr_anz + 1) :

                l_pprice = db_session.query(L_pprice).filter(
                        (L_pprice.artnr == s_artnr) &  (L_pprice.counter == i)).first()

                if l_pprice:

                    l_pprice = db_session.query(L_pprice).first()
                    l_pprice.counter = l_pprice.counter - 1

                    l_pprice = db_session.query(L_pprice).first()

            if created:
                l_price1.counter = curr_anz

                l_price1 = db_session.query(L_price1).first()

        if not created:
            l_pprice = L_pprice()
            db_session.add(l_pprice)

            l_pprice.docu_nr = lscheinnr
            l_pprice.artnr = s_artnr
            l_pprice.anzahl = qty
            l_pprice.einzelpreis = price
            l_pprice.warenwert = qty * price
            l_pprice.bestelldatum = datum
            l_pprice.lief_nr = lief_nr
            l_pprice.counter = curr_anz + 1

            l_pprice = db_session.query(L_pprice).first()

            l_art = db_session.query(L_art).first()
            l_art.lieferfrist = curr_anz + 1

            l_art = db_session.query(L_art).first()

    for op_list in query(op_list_list):
        op_list.docu_nr = lscheinnr
        op_list.lscheinnr = lscheinnr
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        t_amount = t_amount + op_list.warenwert
        curr_lager = op_list.lager_nr

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_artnr)).first()
        create_l_op()

        if rcv_type == 2 and avail_l_out:
            create_l_op1()
        created = True

    if lief_nr != 0 and t_amount != 0:
        get_output(s_stockins_create_apbl(lief_nr, lscheinnr, billdate, t_amount, user_init))

    return generate_output()