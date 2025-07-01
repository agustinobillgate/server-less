#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_ophdr, L_bestand, L_verbrauch, L_artikel

op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string})

def s_transform_btn_gobl(op_list_list:[Op_list], rec_id:int, curr_lager:int, curr_pos:int, transdate:date, wip_acct:string, to_stock:int, s_artnr1:int, qty1:Decimal, bediener_nr:int):

    prepare_cache ([L_op, L_ophdr, L_bestand, L_verbrauch, L_artikel])

    t_amount = to_decimal("0.0")
    amount = to_decimal("0.0")
    s_artnr = 0
    qty = to_decimal("0.0")
    price = to_decimal("0.0")
    zeit:int = 0
    l_op = l_ophdr = l_bestand = l_verbrauch = l_artikel = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_amount, amount, s_artnr, qty, price, zeit, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr


        nonlocal op_list

        return {"t_amount": t_amount, "amount": amount, "s_artnr": s_artnr, "qty": qty, "price": price}

    def l_op_pos():

        nonlocal t_amount, amount, s_artnr, qty, price, zeit, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr


        nonlocal op_list

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)

        for l_op1 in db_session.query(L_op1).filter(
                 (L_op1.lscheinnr == lscheinnr) & (L_op1.loeschflag >= 0) & (L_op1.pos > 0)).order_by(L_op1._recid).all():

            if l_op1.pos > pos:
                pos = l_op1.pos
        pos = pos + 1

        return generate_inner_output()


    def create_l_op(zeit:int):

        nonlocal t_amount, amount, s_artnr, qty, price, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr


        nonlocal op_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        anz_oh:Decimal = to_decimal("0.0")
        val_oh:Decimal = to_decimal("0.0")

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})
        anz_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
        val_oh =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

        if anz_oh != 0:
            price =  to_decimal(val_oh) / to_decimal(anz_oh)
            wert =  to_decimal(qty) * to_decimal(price)
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        amount =  to_decimal(wert)
        t_amount =  to_decimal(t_amount) + to_decimal(wert)
        pass
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
        pass
        pass

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
        pass
        pass
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = zeit
        l_op.anzahl =  to_decimal(anzahl)
        l_op.einzelpreis =  to_decimal(price)
        l_op.warenwert =  to_decimal(wert)
        l_op.op_art = 4
        l_op.herkunftflag = 3
        l_op.lscheinnr = lscheinnr
        l_op.stornogrund = wip_acct
        l_op.pos = 1
        l_op.fuellflag = bediener_nr


        pass

        l_verbrauch = get_cache (L_verbrauch, {"artnr": [(eq, s_artnr)],"datum": [(eq, transdate)]})

        if not l_verbrauch:
            l_verbrauch = L_verbrauch()
            db_session.add(l_verbrauch)

            l_verbrauch.artnr = s_artnr
            l_verbrauch.datum = transdate
        l_verbrauch.anz_verbrau =  to_decimal(l_verbrauch.anz_verbrau) + to_decimal(anzahl)
        l_verbrauch.wert_verbrau =  to_decimal(l_verbrauch.wert_verbrau) + to_decimal(wert)
        pass


    def create_transin():

        nonlocal t_amount, amount, s_artnr, qty, price, zeit, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr


        nonlocal op_list

        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = to_stock
        l_op.artnr = s_artnr1
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl =  to_decimal(qty1)
        l_op.einzelpreis = ( to_decimal(t_amount) / to_decimal(qty1) )
        l_op.warenwert =  to_decimal(t_amount)
        l_op.op_art = 2
        l_op.herkunftflag = 3
        l_op.lscheinnr = lscheinnr
        l_op.pos = 1
        l_op.stornogrund = wip_acct
        l_op.fuellflag = bediener_nr


        pass

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr1)]})

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr1
            l_bestand.anf_best_dat = transdate
        l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(qty1)
        l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(t_amount)
        pass
        tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
        tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, to_stock)],"artnr": [(eq, s_artnr1)]})

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr1
            l_bestand.lager_nr = to_stock
            l_bestand.anf_best_dat = transdate
        l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(qty1)
        l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(t_amount)
        pass

        if tot_anz != 0:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr1)]})
            l_artikel.vk_preis =  to_decimal(tot_val) / to_decimal(tot_anz)
            pass


    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, rec_id)]})
    pass
    l_ophdr.datum = transdate
    l_ophdr.lager_nr = curr_lager
    pass
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    zeit = get_current_time_in_seconds()
    t_amount =  to_decimal("0")

    for op_list in query(op_list_list, filters=(lambda op_list: op_list.anzahl != 0)):
        zeit = zeit + 1
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        curr_lager = op_list.lager_nr
        create_l_op(zeit)
    create_transin()

    return generate_output()