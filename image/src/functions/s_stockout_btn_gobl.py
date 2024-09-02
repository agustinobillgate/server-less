from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_ophdr, L_bestand, L_verbrauch, L_artikel

def s_stockout_btn_gobl(op_list:[Op_list], pvilanguage:int, out_type:int, rec_id:int, curr_lager:int, jobnr:int, cost_acct:str, transdate:date, t_datum:date, transfered:bool, t_lschein:str, to_stock:int, lscheinnr:str, bediener_nr:int, qty:decimal, t_amount:decimal):
    s_artnr = 0
    err_flag = 0
    price = 0
    amount = 0
    msg_str2 = ""
    msg_str3 = ""
    req_created = False
    lvcarea:str = "s_stockout"
    curr_pos:int = 0
    zeit:int = 0
    its_ok:bool = False
    l_op = l_ophdr = l_bestand = l_verbrauch = l_artikel = None

    op_list = out_list = l_op1 = bbuff = lbuff = None

    op_list_list, Op_list = create_model_like(L_op, {"fibu":str, "a_bezeich":str, "a_lief_einheit":decimal, "a_traubensort":str})
    out_list_list, Out_list = create_model("Out_list", {"artnr":int})

    L_op1 = L_op
    Bbuff = L_bestand
    Lbuff = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, its_ok, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1, bbuff, lbuff


        nonlocal op_list, out_list, l_op1, bbuff, lbuff
        nonlocal op_list_list, out_list_list
        return {"s_artnr": s_artnr, "err_flag": err_flag, "price": price, "amount": amount, "msg_str2": msg_str2, "msg_str3": msg_str3, "req_created": req_created}

    def create_l_op(zeit:int):

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, its_ok, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1, bbuff, lbuff


        nonlocal op_list, out_list, l_op1, bbuff, lbuff
        nonlocal op_list_list, out_list_list

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

        if not transfered:

            l_bestand = db_session.query(L_bestand).first()
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

            l_bestand = db_session.query(L_bestand).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()
        l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
        l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

        l_bestand = db_session.query(L_bestand).first()

        if transfered:

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == to_stock) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.anf_best_dat = transdate
                l_bestand.artnr = s_artnr
                l_bestand.lager_nr = to_stock
            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert

            l_bestand = db_session.query(L_bestand).first()
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = op_list.zeit
        l_op.anzahl = anzahl
        l_op.einzelpreis = price
        l_op.warenwert = wert

        if not transfered:
            l_op.op_art = 3
        else:
            l_op.op_art = 4
        l_op.herkunftflag = 1
        l_op.lscheinnr = lscheinnr

        if not transfered:
            l_op.pos = curr_pos

            if op_list.fibu != "":
                l_op.stornogrund = op_list.fibu
            else:
                l_op.stornogrund = cost_acct
        else:
            l_op.pos = to_stock
        l_op.fuellflag = bediener_nr

        l_op = db_session.query(L_op).first()

        if transfered:
            l_op = L_op()
            db_session.add(l_op)

            l_op.datum = transdate
            l_op.lager_nr = to_stock
            l_op.artnr = s_artnr
            l_op.zeit = op_list.zeit
            l_op.anzahl = anzahl
            l_op.einzelpreis = price
            l_op.warenwert = wert
            l_op.op_art = 2
            l_op.herkunftflag = 1
            l_op.lscheinnr = lscheinnr
            l_op.pos = curr_lager
            l_op.fuellflag = bediener_nr

            l_op = db_session.query(L_op).first()

        if not transfered:

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

    def l_op_pos():

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, its_ok, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1, bbuff, lbuff


        nonlocal op_list, out_list, l_op1, bbuff, lbuff
        nonlocal op_list_list, out_list_list

        pos = 0

        def generate_inner_output():
            return pos
        L_op1 = L_op

        for l_op1 in db_session.query(L_op1).filter(
                (func.lower(L_op1.(lscheinnr).lower()) == (lscheinnr).lower()) &  (L_op1.loeschflag >= 0) &  (L_op1.pos > 0)).all():

            if l_op1.pos > pos:
                pos = l_op1.pos
        pos = pos + 1


        return generate_inner_output()

    def check_min_oh():

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, its_ok, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1, bbuff, lbuff


        nonlocal op_list, out_list, l_op1, bbuff, lbuff
        nonlocal op_list_list, out_list_list

        curr_oh:decimal = 0
        Bbuff = L_bestand

        for op_list in query(op_list_list):

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == op_list.artnr)).first()

            if l_artikel.min_bestand != 0:

                for l_bestand in db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr > 0)).all():
                    curr_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if curr_oh < l_artikel.min_best:
                        msg_str2 = msg_str2 + "&W" + translateExtended ("One (or more) stock item(s) under Minimum Onhand Level!", lvcarea, "") + chr(10) + to_string(l_artikel.artnr) + " " + l_artikel.bezeich + chr(10) + translateExtended ("Current Onhand:", lvcarea, "") + " " + to_string(curr_oh) + " <> " + translateExtended ("Minimum Onhand:", lvcarea, "") + " " + to_string(l_artikel.min_best)
                        break


    def check_qty():

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, its_ok, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1, bbuff, lbuff


        nonlocal op_list, out_list, l_op1, bbuff, lbuff
        nonlocal op_list_list, out_list_list

        its_ok = False
        curr_oh:decimal = 0

        def generate_inner_output():
            return its_ok

        for op_list in query(op_list_list):

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr == op_list.artnr) &  (L_bestand.lager_nr == op_list.lager_nr)).first()
            curr_oh = anz_anf_best + anz_eingang - anz_ausgang

            if curr_oh < op_list.anzahl:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == op_list.artnr)).first()
                msg_str3 = msg_str3 + translateExtended ("Wrong quantity: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr(10) + translateExtended ("Inputted quantity  == ", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand  == ", lvcarea, "") + " " + to_string(curr_oh) + chr(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
                its_ok = False

                return generate_inner_output()


        return generate_inner_output()

    def update_request_records():

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, its_ok, l_op, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal l_op1, bbuff, lbuff


        nonlocal op_list, out_list, l_op1, bbuff, lbuff
        nonlocal op_list_list, out_list_list

        op_num:int = 13
        Lbuff = L_op

        if out_type == 1:
            op_num = 14
        req_created = True

        l_op = db_session.query(L_op).filter(
                (L_op.datum == t_datum) &  (L_op.op_art == op_num) &  (func.lower(L_op.lscheinnr) == (t_lschein).lower())).first()
        while None != l_op:

            op_list = query(op_list_list, filters=(lambda op_list :op_list.artnr == l_op.artnr), first=True)

            lbuff = db_session.query(Lbuff).filter(
                        (Lbuff._recid == l_op._recid)).first()
            lbuff.herkunftflag = 2

            if op_list:
                lbuff.deci1[0] = op_list.anzahl

            lbuff = db_session.query(Lbuff).first()

            l_op = db_session.query(L_op).filter(
                    (L_op.datum == t_datum) &  (L_op.op_art == op_num) &  (func.lower(L_op.lscheinnr) == (t_lschein).lower())).first()


    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == rec_id)).first()
    check_min_oh()
    its_ok = check_qty()

    if not its_ok:

        return generate_output()

    l_ophdr = db_session.query(L_ophdr).first()
    l_ophdr.datum = transdate
    l_ophdr.lager_nr = curr_lager

    if not transfered:
        l_ophdr.fibukonto = cost_acct
        l_ophdr.betriebsnr = jobnr

    l_ophdr = db_session.query(L_ophdr).first()

    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    zeit = get_current_time_in_seconds()

    for op_list in query(op_list_list, filters=(lambda op_list :op_list.anzahl != 0)):
        zeit = zeit + 1
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        curr_lager = op_list.lager_nr
        cost_acct = op_list.fibu
        create_l_op(zeit)
    out_list_list.clear()

    if t_lschein != "":
        update_request_records()
    op_list_list.clear()

    return generate_output()