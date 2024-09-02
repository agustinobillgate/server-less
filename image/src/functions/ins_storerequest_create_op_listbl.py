from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, Bediener, L_artikel, L_bestand, H_rezlin

def ins_storerequest_create_op_listbl(out_list:[Out_list], op_list:[Op_list], amount:decimal, t_amount:decimal, pvilanguage:int, user_init:str, s_artnr:int, qty:decimal, transfered:bool, cost_acct:str, curr_lager:int, price:decimal, transdate:date, lscheinnr:str):
    err_flag2 = 0
    err_flag1 = 0
    err_flag = 0
    oh_ok = False
    msg_str2 = ""
    lvcarea:str = "ins_storerequest"
    anzahl:decimal = 0
    wert:decimal = 0
    l_op = bediener = l_artikel = l_bestand = h_rezlin = None

    op_list = op_list1 = out_list = sys_user = l_artikel = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str, "onhand":decimal, "new_flag":bool}, {"new_flag": True})
    op_list1_list, Op_list1 = create_model_like(Op_list)
    out_list_list, Out_list = create_model("Out_list", {"artnr":int})

    Sys_user = Bediener
    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag2, err_flag1, err_flag, oh_ok, msg_str2, lvcarea, anzahl, wert, l_op, bediener, l_artikel, l_bestand, h_rezlin
        nonlocal sys_user, l_artikel


        nonlocal op_list, op_list1, out_list, sys_user, l_artikel
        nonlocal op_list_list, op_list1_list, out_list_list
        return {"err_flag2": err_flag2, "err_flag1": err_flag1, "err_flag": err_flag, "oh_ok": oh_ok, "msg_str2": msg_str2}

    def create_op_list1(p_artnr:int, menge:decimal, oh_ok:bool):

        nonlocal err_flag2, err_flag1, err_flag, msg_str2, lvcarea, anzahl, wert, l_op, bediener, l_artikel, l_bestand, h_rezlin
        nonlocal sys_user, l_artikel


        nonlocal op_list, op_list1, out_list, sys_user, l_artikel
        nonlocal op_list_list, op_list1_list, out_list_list

        stock_oh:decimal = 0
        inh:decimal = 0
        L_art = L_artikel

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():
            inh = menge * h_rezlin.menge

            if h_rezlin.recipe_flag :
                create_op_list1(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_art).filter(
                        (L_art.artnr == h_rezlin.artnrlager)).first()

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == h_rezlin.artnrlager)).first()

                if not l_bestand:
                    err_flag2 = 1
                    msg_str2 = translateExtended ("Article ", lvcarea, "") + to_string(l_artikel.artnr, "9999999") + " - " + l_artikel.bezeich + " not found, posting not possible."
                    oh_ok = False

                    return
                stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
                inh = inh / l_artikel.inhalt

                if inh > stock_oh:
                    err_flag2 = 2
                    msg_str2 = translateExtended ("Quantity over stock_onhand: ", lvcarea, "") + to_string(l_artikel.artnr, "9999999") + " - " + l_artikel.bezeich + chr(10) + "  (" + to_string(inh) + " > " + to_string(stock_oh) + translateExtended ("), posting not possible.", lvcarea, "")
                    oh_ok = False

                    return
                amount = inh * l_artikel.vk_preis / (1 - h_rezlin.lostfact / 100)
                t_amount = t_amount + amount
                op_list1 = Op_list1()
                op_list1_list.append(op_list1)

                op_list1.datum = transdate
                op_list1.lager_nr = curr_lager
                op_list1.artnr = l_artikel.artnr
                op_list1.zeit = get_current_time_in_seconds()
                op_list1.anzahl = inh
                op_list1.einzelpreis = l_artikel.vk_preis
                op_list1.warenwert = amount
                op_list1.op_art = 13
                op_list1.herkunftflag = 1
                op_list1.lscheinnr = lscheinnr
                op_list1.fuellflag = bediener.nr
                op_list1.pos = 1

                l_artikel = db_session.query(L_art).filter(
                        (L_art.artnr == op_list1.artnr)).first()

                sys_user = db_session.query(Sys_user).filter(
                        (Sys_user.nr == op_list1.fuellflag)).first()

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == op_list.artnr) &  (L_bestand.lager_nr == curr_lager)).first()
                op_list1.bezeich = l_artikel.bezeich
                op_list1.username = sys_user.username

                if l_bestand:
                    op_list1.onhand = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if l_artikel.betriebsnr > 0:
        op_list1_list.clear()
        oh_ok = create_op_list1(l_artikel.betriebsnr, qty, oh_ok)

        if oh_ok:

            for op_list1 in query(op_list1_list):
                op_list = Op_list()
                op_list_list.append(op_list)

                buffer_copy(op_list1, op_list)

                if not transfered:
                    op_list.stornogrund = cost_acct
            err_flag1 = 1
        err_flag = 1

        return generate_output()
    anzahl = qty
    wert = qty * price
    amount = wert
    t_amount = t_amount + wert

    if curr_lager == 0:

        return generate_output()
    op_list = Op_list()
    op_list_list.append(op_list)

    op_list.datum = transdate
    op_list.lager_nr = curr_lager
    op_list.artnr = s_artnr
    op_list.zeit = get_current_time_in_seconds()
    op_list.anzahl = anzahl
    op_list.einzelpreis = price
    op_list.warenwert = wert
    op_list.herkunftflag = 1
    op_list.lscheinnr = lscheinnr
    op_list.fuellflag = bediener.nr
    op_list.pos = 1

    if transfered:
        op_list.op_art = 14
    else:
        op_list.op_art = 13

    if not transfered:
        op_list.stornogrund = cost_acct

    l_artikel = db_session.query(L_artikel).filter(
            (l_artikel.artnr == op_list.artnr)).first()

    sys_user = db_session.query(Sys_user).filter(
            (Sys_user.nr == op_list.fuellflag)).first()

    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.artnr == op_list.artnr) &  (L_bestand.lager_nr == curr_lager)).first()
    op_list.bezeich = l_artikel.bezeich
    op_list.username = sys_user.username

    if l_bestand:
        op_list.onhand = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
    out_list = Out_list()
    out_list_list.append(out_list)

    out_list.artnr = l_artikel.artnr

    return generate_output()