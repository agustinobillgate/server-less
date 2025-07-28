#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 28/7/2025
# gitlab: 556
# payload:
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, L_artikel, L_bestand, H_rezlin

out_list_data, Out_list = create_model("Out_list", {"artnr":int})
op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "new_flag":bool}, {"new_flag": True})

def ins_storerequest_create_op_listbl(out_list_data:[Out_list], op_list_data:[Op_list], amount:Decimal, t_amount:Decimal, pvilanguage:int, user_init:string, s_artnr:int, qty:Decimal, transfered:bool, cost_acct:string, curr_lager:int, price:Decimal, transdate:date, lscheinnr:string):

    prepare_cache ([Bediener, L_artikel, L_bestand, H_rezlin])

    err_flag2 = 0
    err_flag1 = 0
    err_flag = 0
    oh_ok = True
    msg_str2 = ""
    lvcarea:string = "ins-storerequest"
    anzahl:Decimal = to_decimal("0.0")
    wert:Decimal = to_decimal("0.0")
    l_op = bediener = l_artikel = l_bestand = h_rezlin = None

    op_list = op_list1 = out_list = sys_user = None

    op_list1_data, Op_list1 = create_model_like(Op_list)

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag2, err_flag1, err_flag, oh_ok, msg_str2, lvcarea, anzahl, wert, l_op, bediener, l_artikel, l_bestand, h_rezlin
        nonlocal amount, t_amount, pvilanguage, user_init, s_artnr, qty, transfered, cost_acct, curr_lager, price, transdate, lscheinnr
        nonlocal sys_user


        nonlocal op_list, op_list1, out_list, sys_user
        nonlocal op_list1_data

        return {"out-list": out_list_data, "op-list": op_list_data, "amount": amount, "t_amount": t_amount, "err_flag2": err_flag2, "err_flag1": err_flag1, "err_flag": err_flag, "oh_ok": oh_ok, "msg_str2": msg_str2}

    def create_op_list1(p_artnr:int, menge:Decimal, oh_ok:bool):

        nonlocal err_flag2, err_flag1, err_flag, msg_str2, lvcarea, anzahl, wert, l_op, bediener, l_artikel, l_bestand, h_rezlin
        nonlocal amount, t_amount, pvilanguage, user_init, s_artnr, qty, transfered, cost_acct, curr_lager, price, transdate, lscheinnr
        nonlocal sys_user


        nonlocal op_list, op_list1, out_list, sys_user
        nonlocal op_list1_data

        stock_oh:Decimal = to_decimal("0.0")
        inh:Decimal = to_decimal("0.0")
        l_artikel = None

        def generate_inner_output():
            return (oh_ok)

        L_art =  create_buffer("L_art",L_artikel)

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                create_op_list1(h_rezlin.artnrlager, inh)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, h_rezlin.artnrlager)]})

                if not l_bestand:
                    err_flag2 = 1
                    msg_str2 = translateExtended ("Article ", lvcarea, "") + to_string(l_artikel.artnr, "9999999") + " - " + l_artikel.bezeich + " not found, posting not possible."
                    oh_ok = False

                    return generate_inner_output()
                stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                inh =  to_decimal(inh) / to_decimal(l_artikel.inhalt)

                if inh > stock_oh:
                    err_flag2 = 2
                    msg_str2 = translateExtended ("Quantity over stock-onhand: ", lvcarea, "") + to_string(l_artikel.artnr, "9999999") + " - " + l_artikel.bezeich + chr_unicode(10) + " (" + to_string(inh) + " > " + to_string(stock_oh) + translateExtended ("), posting not possible.", lvcarea, "")
                    oh_ok = False

                    return generate_inner_output()
                amount =  to_decimal(inh) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                t_amount =  to_decimal(t_amount) + to_decimal(amount)
                op_list1 = Op_list1()
                op_list1_data.append(op_list1)

                op_list1.datum = transdate
                op_list1.lager_nr = curr_lager
                op_list1.artnr = l_artikel.artnr
                op_list1.zeit = get_current_time_in_seconds()
                op_list1.anzahl =  to_decimal(inh)
                op_list1.einzelpreis =  to_decimal(l_artikel.vk_preis)
                op_list1.warenwert =  to_decimal(amount)
                op_list1.op_art = 13
                op_list1.herkunftflag = 1
                op_list1.lscheinnr = lscheinnr
                op_list1.fuellflag = bediener.nr
                op_list1.pos = 1

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, op_list1.artnr)]})

                sys_user = get_cache (Bediener, {"nr": [(eq, op_list1.fuellflag)]})

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list.artnr)],"lager_nr": [(eq, curr_lager)]})
                op_list1.bezeich = l_artikel.bezeich
                op_list1.username = sys_user.username

                if l_bestand:
                    op_list1.onhand =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

        return generate_inner_output()


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    # Rd 28/7/2025
    # add if available
    # if l_artikel.betriebsnr > 0:
    if l_artikel and l_artikel.betriebsnr > 0:
        op_list1_data.clear()
        oh_ok = create_op_list1(l_artikel.betriebsnr, qty, oh_ok)

        if oh_ok:

            for op_list1 in query(op_list1_data):
                op_list = Op_list()
                op_list_data.append(op_list)

                buffer_copy(op_list1, op_list)

                if not transfered:
                    op_list.stornogrund = cost_acct
            err_flag1 = 1
        err_flag = 1

        return generate_output()
    anzahl =  to_decimal(qty)
    wert =  to_decimal(qty) * to_decimal(price)
    amount =  to_decimal(wert)
    t_amount =  to_decimal(t_amount) + to_decimal(wert)

    if curr_lager == 0:

        return generate_output()
    op_list = Op_list()
    op_list_data.append(op_list)

    op_list.datum = transdate
    op_list.lager_nr = curr_lager
    op_list.artnr = s_artnr
    op_list.zeit = get_current_time_in_seconds()
    op_list.anzahl =  to_decimal(anzahl)
    op_list.einzelpreis =  to_decimal(price)
    op_list.warenwert =  to_decimal(wert)
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

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, op_list.artnr)]})

    sys_user = get_cache (Bediener, {"nr": [(eq, op_list.fuellflag)]})

    l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list.artnr)],"lager_nr": [(eq, curr_lager)]})
    op_list.bezeich = l_artikel.bezeich
    op_list.username = sys_user.username

    if l_bestand:
        op_list.onhand =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
    out_list = Out_list()
    out_list_data.append(out_list)

    out_list.artnr = l_artikel.artnr

    return generate_output()