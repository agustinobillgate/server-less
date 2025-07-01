#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.s_stockout_h_rezlinbl import s_stockout_h_rezlinbl
from functions.s_stockout_create_op_list1bl import s_stockout_create_op_list1bl
from models import L_bestand, H_rezlin, L_op, L_artikel

def s_stockout_create_op_list_webbl(s_artnr:int, curr_lager:int, lscheinnr:string, transdate:date, qty:Decimal, cost_acct:string, a_bez:string, transfered:bool, tp_bediener_nr:int):

    prepare_cache ([L_artikel])

    msg_str = ""
    op_list_list = []
    amount:Decimal = to_decimal("0.0")
    t_amount:Decimal = to_decimal("0.0")
    price:Decimal = to_decimal("0.0")
    description:string = ""
    l_bestand = h_rezlin = l_op = l_artikel = None

    t_l_bestand = t_h_rezlin = temp_l_artikel = op_list = op_list1 = l_art = None

    t_l_bestand_list, T_l_bestand = create_model_like(L_bestand)
    t_h_rezlin_list, T_h_rezlin = create_model_like(H_rezlin)
    temp_l_artikel_list, Temp_l_artikel = create_model("Temp_l_artikel", {"artnr":int, "bezeich":string, "betriebsnr":int, "endkum":int, "masseinheit":string, "vk_preis":Decimal, "inhalt":Decimal, "lief_einheit":Decimal, "traubensort":string})
    op_list_list, Op_list = create_model_like(L_op, {"fibu":string, "a_bezeich":string, "a_lief_einheit":Decimal, "a_traubensort":string})
    op_list1_list, Op_list1 = create_model_like(L_op, {"a_lief_einheit":Decimal, "a_traubensort":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, op_list_list, amount, t_amount, price, description, l_bestand, h_rezlin, l_op, l_artikel
        nonlocal s_artnr, curr_lager, lscheinnr, transdate, qty, cost_acct, a_bez, transfered, tp_bediener_nr


        nonlocal t_l_bestand, t_h_rezlin, temp_l_artikel, op_list, op_list1, l_art
        nonlocal t_l_bestand_list, t_h_rezlin_list, temp_l_artikel_list, op_list_list, op_list1_list

        return {"msg_str": msg_str, "op-list": op_list_list}

    def create_op_list():

        nonlocal msg_str, op_list_list, amount, t_amount, price, description, l_bestand, h_rezlin, l_op, l_artikel
        nonlocal s_artnr, curr_lager, lscheinnr, transdate, qty, cost_acct, a_bez, transfered, tp_bediener_nr


        nonlocal t_l_bestand, t_h_rezlin, temp_l_artikel, op_list, op_list1, l_art
        nonlocal t_l_bestand_list, t_h_rezlin_list, temp_l_artikel_list, op_list_list, op_list1_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        oh_ok:bool = True

        if l_artikel.betriebsnr > 0:
            op_list1_list.clear()
            t_l_bestand_list, t_h_rezlin_list = get_output(s_stockout_h_rezlinbl(l_artikel.betriebsnr, curr_lager))
            oh_ok = create_op_list1(l_artikel.betriebsnr, qty, oh_ok)

            if oh_ok:

                for op_list1 in query(op_list1_list):
                    op_list = Op_list()
                    op_list_list.append(op_list)

                    op_list.datum = op_list1.datum
                    op_list.lager_nr = op_list1.lager_nr
                    op_list.artnr = op_list1.artnr
                    op_list.zeit = op_list1.zeit
                    op_list.anzahl =  to_decimal(op_list1.anzahl)
                    op_list.einzelpreis =  to_decimal(op_list1.einzelpreis)
                    op_list.warenwert =  to_decimal(op_list1.warenwert)
                    op_list.op_art = op_list1.op_art
                    op_list.herkunftflag = op_list1.herkunftflag
                    op_list.lscheinnr = op_list1.lscheinnr
                    op_list.fuellflag = op_list1.fuellflag
                    op_list.pos = op_list1.pos
                    op_list.a_lief_einheit =  to_decimal(op_list1.a_lief_einheit)
                    op_list.a_traubensort = op_list1.a_traubensort
                    op_list.fibu = cost_acct
                    op_list.stornogrund = a_bez

            return
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        amount =  to_decimal(wert)
        t_amount =  to_decimal(t_amount) + to_decimal(wert)

        if curr_lager == 0:

            return
        op_list = Op_list()
        op_list_list.append(op_list)

        op_list.datum = transdate
        op_list.lager_nr = curr_lager
        op_list.artnr = s_artnr
        op_list.zeit = get_current_time_in_seconds()
        op_list.anzahl =  to_decimal(anzahl)
        op_list.einzelpreis =  to_decimal(price)
        op_list.warenwert =  to_decimal(wert)
        op_list.herkunftflag = 1
        op_list.lscheinnr = lscheinnr
        op_list.fuellflag = tp_bediener_nr
        op_list.pos = 1
        op_list.a_bezeich = description
        op_list.fibu = cost_acct
        op_list.stornogrund = a_bez

        if transfered:
            op_list.op_art = 4
        else:
            op_list.op_art = 3

        if not transfered:
            op_list.fibu = cost_acct


    def create_op_list1(p_artnr:int, menge:Decimal, oh_ok:bool):

        nonlocal msg_str, op_list_list, amount, t_amount, price, description, l_bestand, h_rezlin, l_op, l_artikel
        nonlocal s_artnr, curr_lager, lscheinnr, transdate, qty, cost_acct, a_bez, transfered, tp_bediener_nr


        nonlocal t_l_bestand, t_h_rezlin, temp_l_artikel, op_list, op_list1, l_art
        nonlocal t_l_bestand_list, t_h_rezlin_list, temp_l_artikel_list, op_list_list, op_list1_list

        stock_oh:Decimal = to_decimal("0.0")
        inh:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (oh_ok)

        L_art = Temp_l_artikel
        l_art_list = temp_l_artikel_list
        temp_l_artikel_list.clear()
        temp_l_artikel_list = get_output(s_stockout_create_op_list1bl(p_artnr))

        for t_h_rezlin in query(t_h_rezlin_list):
            inh =  to_decimal(menge) * to_decimal(t_h_rezlin.menge)

            if t_h_rezlin.recipe_flag :
                oh_ok = create_op_list1(t_h_rezlin.artnrlager, inh, oh_ok)

                if not oh_ok:

                    return generate_inner_output()
            else:

                l_art = query(l_art_list, filters=(lambda l_art: l_art.artnr == t_h_rezlin.artnrlager), first=True)

                t_l_bestand = query(t_l_bestand_list, filters=(lambda t_l_bestand: t_l_bestand.lager_nr == curr_lager and t_l_bestand.artnr == t_h_rezlin.artnrlager), first=True)

                if not t_l_bestand:
                    msg_str = "Article " + to_string(l_art.artnr, "9999999") + " - " + l_art.bezeich + " not found, posting not possible."
                    oh_ok = False

                    return generate_inner_output()
                stock_oh =  to_decimal(t_l_bestand.anz_anf_best) + to_decimal(t_l_bestand.anz_eingang) - to_decimal(t_l_bestand.anz_ausgang)
                inh =  to_decimal(inh) / to_decimal(l_art.inhalt)

                if inh > stock_oh:
                    msg_str = "Quantity over stock-onhand: " + to_string(l_art.artnr, "9999999") + " - " + l_art.bezeich + " " + to_string(inh) + " > " + to_string(stock_oh) + ", posting not possible."
                    oh_ok = False

                    return generate_inner_output()
                amount =  to_decimal(inh) * to_decimal(l_art.vk_preis) / to_decimal((1) - to_decimal(t_h_rezlin.lostfact) / to_decimal(100))
                t_amount =  to_decimal(t_amount) + to_decimal(amount)
                op_list1 = Op_list1()
                op_list1_list.append(op_list1)

                op_list1.datum = transdate
                op_list1.lager_nr = curr_lager
                op_list1.artnr = l_art.artnr
                op_list1.zeit = get_current_time_in_seconds()
                op_list1.anzahl =  to_decimal(inh)
                op_list1.einzelpreis =  to_decimal(l_art.vk_preis)
                op_list1.warenwert =  to_decimal(amount)
                op_list1.op_art = 3
                op_list1.herkunftflag = 1
                op_list1.lscheinnr = lscheinnr
                op_list1.fuellflag = tp_bediener_nr
                op_list1.pos = 1
                op_list1.a_lief_einheit =  to_decimal(l_art.lief_einheit)
                op_list1.a_traubensort = l_art.traubensorte

        return generate_inner_output()


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if l_artikel:
        description = l_artikel.bezeich + " - " + l_artikel.masseinheit
        price =  to_decimal(l_artikel.vk_preis)


        create_op_list()

    return generate_output()