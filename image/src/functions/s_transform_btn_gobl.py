from functions.additional_functions import *
import decimal
from datetime import date
from models import L_op, L_ophdr, L_bestand, L_verbrauch, L_artikel

def s_transform_btn_gobl(op_list:[Op_list], rec_id:int, curr_lager:int, curr_pos:int, transdate:date, wip_acct:str, to_stock:int, s_artnr1:int, qty1:decimal, bediener_nr:int):
    t_amount = 0
    amount = 0
    s_artnr = 0
    qty = 0
    price = 0
    zeit:int = 0
    l_op = l_ophdr = l_bestand = l_verbrauch = l_artikel = None

    op_list = l_op1 = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str})

    L_op1 = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_amount, amount, s_artnr, qty, price, zeit, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list
        return {"t_amount": t_amount, "amount": amount, "s_artnr": s_artnr, "qty": qty, "price": price}

    def l_op_pos():

        nonlocal t_amount, amount, s_artnr, qty, price, zeit, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list

        pos = 0

        def generate_inner_output():
            return pos
        L_op1 = L_op

        for l_op1 in db_session.query(L_op1).filter(
                (L_op1.lscheinnr == lscheinnr) &  (L_op1.loeschflag >= 0) &  (L_op1.pos > 0)).all():

            if l_op1.pos > pos:
                pos = l_op1.pos
        pos = pos + 1


        return generate_inner_output()

    def create_l_op(zeit:int):

        nonlocal t_amount, amount, s_artnr, qty, price, zeit, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        anz_oh:decimal = 0
        val_oh:decimal = 0

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()
        anz_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
        val_oh = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

        if anz_oh != 0:
            price = val_oh / anz_oh
            wert = qty * price
        anzahl = qty
        wert = qty * price
        amount = wert
        t_amount = t_amount + wert

        l_bestand = db_session.query(L_bestand).first()
        l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
        l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

        l_bestand = db_session.query(L_bestand).first()


        l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()
        l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
        l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

        l_bestand = db_session.query(L_bestand).first()

        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = zeit
        l_op.anzahl = anzahl
        l_op.einzelpreis = price
        l_op.warenwert = wert
        l_op.op_art = 4
        l_op.herkunftflag = 3
        l_op.lscheinnr = lscheinnr
        l_op.stornogrund = wip_acct
        l_op.pos = 1
        l_op.fuellflag = bediener_nr

        l_op = db_session.query(L_op).first()

        l_verbrauch = db_session.query(L_verbrauch).filter(
                    (L_verbrauch.artnr == s_artnr) &  (L_verbrauch.datum == transdate)).first()

        if not l_verbrauch:
            l_verbrauch = L_verbrauch()
            db_session.add(l_verbrauch)

            l_verbrauch.artnr = s_artnr
            l_verbrauch.datum = transdate
        l_verbrauch.anz_verbrau = l_verbrauch.anz_verbrau + anzahl
        l_verbrauch.wert_verbrau = l_verbrauch.wert_verbrau + wert

        l_verbrauch = db_session.query(L_verbrauch).first()

    def create_transin():

        nonlocal t_amount, amount, s_artnr, qty, price, zeit, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list

        tot_anz:decimal = 0
        tot_val:decimal = 0
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = to_stock
        l_op.artnr = s_artnr1
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl = qty1
        l_op.einzelpreis = (t_amount / qty1)
        l_op.warenwert = t_amount
        l_op.op_art = 2
        l_op.herkunftflag = 3
        l_op.lscheinnr = lscheinnr
        l_op.pos = 1
        l_op.stornogrund = wip_acct
        l_op.fuellflag = bediener_nr

        l_op = db_session.query(L_op).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr1)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr1
            l_bestand.anf_best_dat = transdate
        l_bestand.anz_eingang = l_bestand.anz_eingang + qty1
        l_bestand.wert_eingang = l_bestand.wert_eingang + t_amount

        l_bestand = db_session.query(L_bestand).first()
        tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
        tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == to_stock) &  (L_bestand.artnr == s_artnr1)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = s_artnr1
            l_bestand.lager_nr = to_stock
            l_bestand.anf_best_dat = transdate
        l_bestand.anz_eingang = l_bestand.anz_eingang + qty1
        l_bestand.wert_eingang = l_bestand.wert_eingang + t_amount

        l_bestand = db_session.query(L_bestand).first()

        if tot_anz != 0:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == s_artnr1)).first()
            l_artikel.vk_preis = tot_val / tot_anz

            l_artikel = db_session.query(L_artikel).first()

    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == rec_id)).first()

    l_ophdr = db_session.query(L_ophdr).first()
    l_ophdr.datum = transdate
    l_ophdr.lager_nr = curr_lager

    l_ophdr = db_session.query(L_ophdr).first()

    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    zeit = get_current_time_in_seconds()
    t_amount = 0

    for op_list in query(op_list_list, filters=(lambda op_list :op_list.anzahl != 0)):
        zeit = zeit + 1
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        curr_lager = op_list.lager_nr
        create_l_op(zeit)
    create_transin()

    return generate_output()