#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Gl_acct, L_ophdr, L_bestand, L_verbrauch, L_artikel

op_list_data, Op_list = create_model_like(L_op, {"fibu":string, "a_bezeich":string, "a_lief_einheit":Decimal, "a_traubensort":string})

def s_stockout_btn_gobl(op_list_data:[Op_list], pvilanguage:int, out_type:int, rec_id:int, curr_lager:int, jobnr:int, cost_acct:string, transdate:date, t_datum:date, transfered:bool, t_lschein:string, to_stock:int, lscheinnr:string, bediener_nr:int, qty:Decimal, t_amount:Decimal):

    prepare_cache ([L_op, L_ophdr, L_bestand, L_verbrauch, L_artikel])

    s_artnr = 0
    err_flag = 0
    price = to_decimal("0.0")
    amount = to_decimal("0.0")
    msg_str2 = ""
    msg_str3 = ""
    req_created = False
    lvcarea:string = "s-stockout"
    curr_pos:int = 0
    zeit:int = 0
    gl_notfound:bool = False
    its_ok:bool = False
    l_op = gl_acct = l_ophdr = l_bestand = l_verbrauch = l_artikel = None

    op_list = out_list = None

    out_list_data, Out_list = create_model("Out_list", {"artnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, gl_notfound, its_ok, l_op, gl_acct, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal pvilanguage, out_type, rec_id, curr_lager, jobnr, cost_acct, transdate, t_datum, transfered, t_lschein, to_stock, lscheinnr, bediener_nr, qty, t_amount


        nonlocal op_list, out_list
        nonlocal out_list_data

        return {"op-list": op_list_data, "qty": qty, "t_amount": t_amount, "s_artnr": s_artnr, "err_flag": err_flag, "price": price, "amount": amount, "msg_str2": msg_str2, "msg_str3": msg_str3, "req_created": req_created}

    def create_l_op(zeit:int):

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, gl_notfound, its_ok, l_op, gl_acct, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal pvilanguage, out_type, rec_id, curr_lager, jobnr, cost_acct, transdate, t_datum, transfered, t_lschein, to_stock, lscheinnr, bediener_nr, qty, t_amount


        nonlocal op_list, out_list
        nonlocal out_list_data

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

        if not transfered:
            pass
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
            pass

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
        pass

        if transfered:

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, to_stock)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.anf_best_dat = transdate
                l_bestand.artnr = s_artnr
                l_bestand.lager_nr = to_stock
            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            pass
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = op_list.zeit
        l_op.anzahl =  to_decimal(anzahl)
        l_op.einzelpreis =  to_decimal(price)
        l_op.warenwert =  to_decimal(wert)

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
        pass

        if transfered:
            l_op = L_op()
            db_session.add(l_op)

            l_op.datum = transdate
            l_op.lager_nr = to_stock
            l_op.artnr = s_artnr
            l_op.zeit = op_list.zeit
            l_op.anzahl =  to_decimal(anzahl)
            l_op.einzelpreis =  to_decimal(price)
            l_op.warenwert =  to_decimal(wert)
            l_op.op_art = 2
            l_op.herkunftflag = 1
            l_op.lscheinnr = lscheinnr
            l_op.pos = curr_lager
            l_op.fuellflag = bediener_nr
            pass

        if not transfered:

            l_verbrauch = get_cache (L_verbrauch, {"artnr": [(eq, s_artnr)],"datum": [(eq, transdate)]})

            if not l_verbrauch:
                l_verbrauch = L_verbrauch()
                db_session.add(l_verbrauch)

                l_verbrauch.artnr = s_artnr
                l_verbrauch.datum = transdate
            l_verbrauch.anz_verbrau =  to_decimal(l_verbrauch.anz_verbrau) + to_decimal(anzahl)
            l_verbrauch.wert_verbrau =  to_decimal(l_verbrauch.wert_verbrau) + to_decimal(wert)
            pass


    def l_op_pos():

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, gl_notfound, its_ok, l_op, gl_acct, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal pvilanguage, out_type, rec_id, curr_lager, jobnr, cost_acct, transdate, t_datum, transfered, t_lschein, to_stock, lscheinnr, bediener_nr, qty, t_amount


        nonlocal op_list, out_list
        nonlocal out_list_data

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


    def check_min_oh():

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, gl_notfound, its_ok, l_op, gl_acct, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal pvilanguage, out_type, rec_id, curr_lager, jobnr, cost_acct, transdate, t_datum, transfered, t_lschein, to_stock, lscheinnr, bediener_nr, qty, t_amount


        nonlocal op_list, out_list
        nonlocal out_list_data

        curr_oh:Decimal = to_decimal("0.0")
        bbuff = None
        Bbuff =  create_buffer("Bbuff",L_bestand)

        for op_list in query(op_list_data):

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, op_list.artnr)]})

            if l_artikel.min_bestand != 0:

                for l_bestand in db_session.query(L_bestand).filter(
                         (L_bestand.artnr == l_artikel.artnr) & (L_bestand.lager_nr > 0)).order_by(L_bestand._recid).yield_per(100):
                    curr_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if curr_oh < l_artikel.min_bestand:
                        msg_str2 = msg_str2 + "&W" + translateExtended ("One (or more) stock item(s) under Minimum Onhand Level!", lvcarea, "") + chr_unicode(10) + to_string(l_artikel.artnr) + " " + l_artikel.bezeich + chr_unicode(10) + translateExtended ("Current Onhand:", lvcarea, "") + " " + to_string(curr_oh) + " <> " + translateExtended ("Minimum Onhand:", lvcarea, "") + " " + to_string(l_artikel.min_bestand)
                        break


    def check_qty():

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, gl_notfound, its_ok, l_op, gl_acct, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal pvilanguage, out_type, rec_id, curr_lager, jobnr, cost_acct, transdate, t_datum, transfered, t_lschein, to_stock, lscheinnr, bediener_nr, qty, t_amount


        nonlocal op_list, out_list
        nonlocal out_list_data

        its_ok = True
        curr_oh:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (its_ok)


        for op_list in query(op_list_data):

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list.artnr)],"lager_nr": [(eq, op_list.lager_nr)]})
            curr_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if curr_oh < op_list.anzahl:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, op_list.artnr)]})
                msg_str3 = msg_str3 + translateExtended ("Wrong quantity: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr_unicode(10) + translateExtended ("Inputted quantity =", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand =", lvcarea, "") + " " + to_string(curr_oh) + chr_unicode(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
                its_ok = False

                return generate_inner_output()

        return generate_inner_output()


    def update_request_records():

        nonlocal s_artnr, err_flag, price, amount, msg_str2, msg_str3, req_created, lvcarea, curr_pos, zeit, gl_notfound, its_ok, l_op, gl_acct, l_ophdr, l_bestand, l_verbrauch, l_artikel
        nonlocal pvilanguage, out_type, rec_id, curr_lager, jobnr, cost_acct, transdate, t_datum, transfered, t_lschein, to_stock, lscheinnr, bediener_nr, qty, t_amount


        nonlocal op_list, out_list
        nonlocal out_list_data

        lbuff = None
        op_num:int = 13
        Lbuff =  create_buffer("Lbuff",L_op)

        if out_type == 1:
            op_num = 14
        req_created = True

        l_op = get_cache (L_op, {"datum": [(eq, t_datum)],"op_art": [(eq, op_num)],"lscheinnr": [(eq, t_lschein)]})
        while None != l_op:

            op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == l_op.artnr), first=True)

            lbuff = get_cache (L_op, {"_recid": [(eq, l_op._recid)]})
            lbuff.herkunftflag = 2

            if op_list:
                lbuff.deci1[0] = op_list.anzahl

                if op_list.fibu != "":
                    lbuff.stornogrund = op_list.fibu
                else:
                    lbuff.stornogrund = cost_acct
            pass
            pass

            curr_recid = l_op._recid
            l_op = db_session.query(L_op).filter(
                     (L_op.datum == t_datum) & (L_op.op_art == op_num) & (L_op.lscheinnr == (t_lschein).lower()) & (L_op._recid > curr_recid)).first()

    if not transfered:

        if cost_acct.lower()  != "" and cost_acct.lower()  != ("00000000").lower()  and cost_acct.lower()  != None:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

            if not gl_acct:
                err_flag = 1

                return generate_output()

        for op_list in query(op_list_data, filters=(lambda op_list: op_list.fibu.lower()  != "" and op_list.fibu.lower()  != ("00000000").lower()  and op_list.fibu.lower()  != None)):

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, op_list.fibu)]})

            if not gl_acct:
                gl_notfound = True
                break

        if gl_notfound:
            err_flag = 1

            return generate_output()
    check_min_oh()
    its_ok = check_qty()

    if not its_ok:

        return generate_output()

    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, rec_id)]})

    if l_ophdr:
        pass
        l_ophdr.datum = transdate
        l_ophdr.lager_nr = curr_lager

        if not transfered:
            l_ophdr.fibukonto = cost_acct
            l_ophdr.betriebsnr = jobnr
        pass
        pass
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    zeit = get_current_time_in_seconds()

    for op_list in query(op_list_data, filters=(lambda op_list: op_list.anzahl != 0)):
        zeit = zeit + 1
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        curr_lager = op_list.lager_nr
        cost_acct = op_list.fibu
        create_l_op(zeit)
    out_list_data.clear()

    if t_lschein != "":
        update_request_records()
    op_list_data.clear()

    return generate_output()