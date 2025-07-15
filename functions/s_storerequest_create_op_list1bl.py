#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, L_artikel, H_rezlin, L_bestand, Gl_acct

def s_storerequest_create_op_list1bl(pvilanguage:int, p_artnr:int, menge:Decimal, oh_ok:bool, curr_lager:int, transdate:date, lscheinnr:string, bediener_nr:int):

    prepare_cache ([Bediener, L_artikel, H_rezlin, L_bestand, Gl_acct])

    msg_str = ""
    op_list1_data = []
    lvcarea:string = "s-storerequest"
    amount:Decimal = to_decimal("0.0")
    t_amount:Decimal = to_decimal("0.0")
    l_op = bediener = l_artikel = h_rezlin = l_bestand = gl_acct = None

    op_list = op_list1 = sys_user = None

    op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "acct_bez":string})
    op_list1_data, Op_list1 = create_model_like(Op_list)

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, op_list1_data, lvcarea, amount, t_amount, l_op, bediener, l_artikel, h_rezlin, l_bestand, gl_acct
        nonlocal pvilanguage, p_artnr, menge, oh_ok, curr_lager, transdate, lscheinnr, bediener_nr
        nonlocal sys_user


        nonlocal op_list, op_list1, sys_user
        nonlocal op_list_data, op_list1_data

        return {"oh_ok": oh_ok, "msg_str": msg_str, "op-list1": op_list1_data}

    def create_op_list1():

        nonlocal msg_str, op_list1_data, lvcarea, amount, t_amount, l_op, bediener, l_artikel, h_rezlin, l_bestand, gl_acct
        nonlocal pvilanguage, p_artnr, menge, oh_ok, curr_lager, transdate, lscheinnr, bediener_nr
        nonlocal sys_user


        nonlocal op_list, op_list1, sys_user
        nonlocal op_list_data, op_list1_data

        stock_oh:Decimal = to_decimal("0.0")
        inh:Decimal = to_decimal("0.0")
        l_art = None
        L_art =  create_buffer("L_art",L_artikel)

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                create_op_list1(h_rezlin.artnrlager, inh)
            else:

                l_art = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, h_rezlin.artnrlager)]})

                if not l_bestand:
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("Article ", lvcarea, "") + to_string(l_art.artnr, "9999999") + " - " + l_art.bezeich + " not found, posting not possible."
                    oh_ok = False

                    return
                stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                inh =  to_decimal(inh) / to_decimal(l_art.inhalt)

                if inh > stock_oh:
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("Quantity over stock-onhand: ", lvcarea, "") + to_string(l_art.artnr, "9999999") + " - " + l_art.bezeich + chr_unicode(10) + " (" + to_string(inh) + " > " + to_string(stock_oh) + translateExtended ("), posting not possible.", lvcarea, "")
                    oh_ok = False

                    return
                amount =  to_decimal(inh) * to_decimal(l_art.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                t_amount =  to_decimal(t_amount) + to_decimal(amount)
                op_list1 = Op_list1()
                op_list1_data.append(op_list1)

                op_list1.datum = transdate
                op_list1.lager_nr = curr_lager
                op_list1.artnr = l_art.artnr
                op_list1.zeit = get_current_time_in_seconds()
                op_list1.anzahl =  to_decimal(inh)
                op_list1.einzelpreis =  to_decimal(l_art.vk_preis)
                op_list1.warenwert =  to_decimal(amount)
                op_list1.op_art = 13
                op_list1.herkunftflag = 1
                op_list1.lscheinnr = lscheinnr
                op_list1.fuellflag = bediener_nr
                op_list1.pos = 1

                l_art = get_cache (L_artikel, {"artnr": [(eq, op_list1.artnr)]})

                sys_user = get_cache (Bediener, {"nr": [(eq, op_list1.fuellflag)]})

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list1.artnr)],"lager_nr": [(eq, curr_lager)]})
                op_list1.bezeich = l_art.bezeich
                op_list1.username = sys_user.username

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, op_list1.stornogrund)]})

                if gl_acct:
                    op_list1.acct_bez = gl_acct.bezeich

                if l_bestand:
                    op_list1.onhand =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)


    create_op_list1()

    return generate_output()