#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 04/08/2025
# gitlab: -
# remarks: if available
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_ophdr, L_bestand, L_verbrauch, L_artikel

op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string})

def s_transform_btn_go_1bl(op_list_data:[Op_list], rec_id:int, curr_lager:int, curr_pos:int, transdate:date, wip_acct:string, to_stock:int, s_artnr1:int, qty1:Decimal, bediener_nr:int, lscheinnr:string):

    prepare_cache ([L_op, L_ophdr, L_bestand, L_verbrauch, L_artikel])

    t_amount = to_decimal("0.0")
    amount = to_decimal("0.0")
    s_artnr = 0
    qty = to_decimal("0.0")
    price = to_decimal("0.0")
    zeit:int = 0
    tamount_op2:Decimal = to_decimal("0.0")
    tamount_op4:Decimal = to_decimal("0.0")
    l_op = l_ophdr = l_bestand = l_verbrauch = l_artikel = None

    op_list = b_lop = None

    B_lop = create_buffer("B_lop",L_op)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_amount, amount, s_artnr, qty, price, zeit, tamount_op2, tamount_op4, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr, lscheinnr
        nonlocal b_lop


        nonlocal op_list, b_lop

        return {"t_amount": t_amount, "amount": amount, "s_artnr": s_artnr, "qty": qty, "price": price}

    def l_op_pos():

        nonlocal t_amount, amount, s_artnr, qty, price, zeit, tamount_op2, tamount_op4, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr, lscheinnr
        nonlocal b_lop


        nonlocal op_list, b_lop

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)

        for l_op1 in db_session.query(L_op1).filter(
                 (L_op1.lscheinnr == (lscheinnr).lower()) & (L_op1.loeschflag >= 0) & (L_op1.pos > 0)).order_by(L_op1._recid).all():

            if l_op1.pos > pos:
                pos = l_op1.pos
        pos = pos + 1

        return generate_inner_output()


    def create_l_op(zeit:int):

        nonlocal t_amount, amount, s_artnr, qty, price, tamount_op2, tamount_op4, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr, lscheinnr
        nonlocal b_lop


        nonlocal op_list, b_lop

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        anz_oh:Decimal = to_decimal("0.0")
        val_oh:Decimal = to_decimal("0.0")

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0) & (L_bestand.artnr == s_artnr)).first()
        
        anz_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
        val_oh =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

        if anz_oh != 0:
            price =  to_decimal(val_oh) / to_decimal(anz_oh)
            wert =  to_decimal(qty) * to_decimal(price)

        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        wert = to_decimal(round(wert , 2))
        amount =  to_decimal(wert)
        t_amount =  to_decimal(t_amount) + to_decimal(wert)
        
        db_session.refresh(l_bestand, with_for_update=True)
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
        db_session.flush()

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == s_artnr)).with_for_update().first()
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)

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

        l_verbrauch = db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == s_artnr) & (L_verbrauch.datum == transdate)).with_for_update().first()

        if not l_verbrauch:
            l_verbrauch = L_verbrauch()
            db_session.add(l_verbrauch)

            l_verbrauch.artnr = s_artnr
            l_verbrauch.datum = transdate

        l_verbrauch.anz_verbrau =  to_decimal(l_verbrauch.anz_verbrau) + to_decimal(anzahl)
        l_verbrauch.wert_verbrau =  to_decimal(l_verbrauch.wert_verbrau) + to_decimal(wert)

    def create_transin():

        nonlocal t_amount, amount, s_artnr, qty, price, zeit, tamount_op2, tamount_op4, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr, lscheinnr
        nonlocal b_lop


        nonlocal op_list, b_lop

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

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0) & (L_bestand.artnr == s_artnr1)).with_for_update().first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr1
            l_bestand.anf_best_dat = transdate

        l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(qty1)
        l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(t_amount)
        
        tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
        tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == to_stock) & (L_bestand.artnr == s_artnr1)).with_for_update().first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr1
            l_bestand.lager_nr = to_stock
            l_bestand.anf_best_dat = transdate

        l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(qty1)
        l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(t_amount)

        if tot_anz != 0:
            db_session.refresh(l_bestand, with_for_update=True)
            l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr1)]})
            l_artikel.vk_preis =  to_decimal(tot_val) / to_decimal(tot_anz)
            db_session.flush()


    def re_calculating_finished_goods():

        nonlocal amount, s_artnr, qty, price, zeit, tamount_op2, tamount_op4, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal rec_id, curr_lager, curr_pos, transdate, wip_acct, to_stock, s_artnr1, qty1, bediener_nr, lscheinnr
        nonlocal b_lop


        nonlocal op_list, b_lop

        deliv_number:string = ""
        tot_anz:Decimal = to_decimal("0.0")
        t_amount:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        init_qty:int = 0
        init_warenwrt:Decimal = to_decimal("0.0")
        l_op_buff = None
        L_op_buff =  create_buffer("L_op_buff",L_op)

        l_op_obj_list = {}
        l_op = L_op()
        l_ophdr = L_ophdr()
        for l_op.lscheinnr, l_op.datum, l_op.lager_nr, l_op.artnr, l_op.zeit, l_op.anzahl, l_op.einzelpreis, l_op.warenwert, l_op.op_art, l_op.herkunftflag, l_op.stornogrund, l_op.pos, l_op.fuellflag, l_op._recid, l_ophdr.datum, l_ophdr.lager_nr, l_ophdr._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.lager_nr, L_op.artnr, L_op.zeit, L_op.anzahl, L_op.einzelpreis, L_op.warenwert, L_op.op_art, L_op.herkunftflag, L_op.stornogrund, L_op.pos, L_op.fuellflag, L_op._recid, L_ophdr.datum, L_ophdr.lager_nr, L_ophdr._recid).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower())).filter(
                 (L_op.op_art >= 2) & (L_op.op_art <= 4) & (L_op.herkunftflag == 3) & (L_op.loeschflag < 2) & (L_op.datum == transdate) & (L_op.lager_nr > 0)).order_by(L_op.datum, L_op.lscheinnr, L_op.op_art.desc()).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if deliv_number != l_op.lscheinnr:
                deliv_number = l_op.lscheinnr

                l_op_buff = db_session.query(L_op_buff).filter(
                         (L_op_buff.lscheinnr == (l_op.lscheinnr).lower()) & (L_op_buff.datum == l_op.datum) & (L_op_buff.op_art == 2) & (L_op_buff.herkunftflag == 3) & (L_op_buff.loeschflag >= 0)).order_by(L_op_buff._recid).first()

                if l_op_buff:
                    init_qty = l_op_buff.anzahl
                    init_warenwrt =  to_decimal(l_op_buff.warenwert)
                    
                    db_session.refresh(l_op_buff, with_for_update=True)
                    l_op_buff.warenwert =  to_decimal(tamount_op4)
                    l_op_buff.einzelpreis = ( to_decimal(tamount_op4) / to_decimal(init_qty) )
                    db_session.flush()

                    l_bestand = db_session.query(L_bestand).filter(
                             (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_op_buff.artnr)).with_for_update().first()

                    if not l_bestand:
                        pass
                    else:
                        l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(init_warenwrt) + to_decimal(tamount_op4)
                    
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                    tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

                    l_bestand = db_session.query(L_bestand).filter(
                             (L_bestand.lager_nr == l_op_buff.lager_nr) & (L_bestand.artnr == l_op_buff.artnr)).with_for_update().first()

                    if not l_bestand:
                        pass
                    else:
                        l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(init_warenwrt) + to_decimal(tamount_op4)
                    pass

                    if tot_anz != 0:
                        l_artikel = db_session.query(L_artikel).filter(L_artikel.artnr == l_op_buff.artnr).with_for_update().first()
                        l_artikel.vk_preis =  to_decimal(tot_val) / to_decimal(tot_anz)

    l_ophdr = db_session.query(L_ophdr).filter(L_ophdr._recid == rec_id).first()
    
    db_session.refresh(l_ophdr, with_for_update=True)
    l_ophdr.datum = transdate
    l_ophdr.lager_nr = curr_lager
    db_session.flush()

    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    zeit = get_current_time_in_seconds()
    t_amount =  to_decimal("0")

    for op_list in query(op_list_data, filters=(lambda op_list: op_list.anzahl != 0)):
        zeit = zeit + 1
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        curr_lager = op_list.lager_nr

        create_l_op(zeit)

    create_transin()
    tamount_op4 =  to_decimal("0")
    tamount_op2 =  to_decimal("0")

    for b_lop in db_session.query(B_lop).filter(
             (B_lop.lscheinnr == (lscheinnr).lower()) & (B_lop.datum == transdate) & (B_lop.herkunftflag == 3) & (B_lop.op_art == 4)).order_by(B_lop._recid).all():
        tamount_op4 =  to_decimal(tamount_op4) + to_decimal(b_lop.warenwert)

    for b_lop in db_session.query(B_lop).filter(
             (B_lop.lscheinnr == (lscheinnr).lower()) & (B_lop.datum == transdate) & (B_lop.herkunftflag == 3) & (B_lop.op_art == 2)).order_by(B_lop._recid).all():
        tamount_op2 =  to_decimal(tamount_op2) + to_decimal(b_lop.warenwert)

    if tamount_op4 != tamount_op2:
        re_calculating_finished_goods()

    return generate_output()