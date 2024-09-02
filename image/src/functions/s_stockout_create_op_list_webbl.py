from functions.additional_functions import *
import decimal
from datetime import date
from functions.s_stockout_h_rezlinbl import s_stockout_h_rezlinbl
from functions.s_stockout_create_op_list1bl import s_stockout_create_op_list1bl
from models import L_bestand, H_rezlin, L_op, L_artikel

def s_stockout_create_op_list_webbl(s_artnr:int, curr_lager:int, lscheinnr:str, transdate:date, qty:decimal, cost_acct:str, a_bez:str, transfered:bool, tp_bediener_nr:int):
    msg_str = ""
    op_list_list = []
    amount:decimal = 0
    t_amount:decimal = 0
    price:decimal = 0
    description:str = ""
    l_bestand = h_rezlin = l_op = l_artikel = None

    t_l_bestand = t_h_rezlin = temp_l_artikel = op_list = op_list1 = l_art = None

    t_l_bestand_list, T_l_bestand = create_model_like(L_bestand)
    t_h_rezlin_list, T_h_rezlin = create_model_like(H_rezlin)
    temp_l_artikel_list, Temp_l_artikel = create_model("Temp_l_artikel", {"artnr":int, "bezeich":str, "betriebsnr":int, "endkum":int, "masseinheit":str, "vk_preis":decimal, "inhalt":decimal, "lief_einheit":decimal, "traubensort":str})
    op_list_list, Op_list = create_model_like(L_op, {"fibu":str, "a_bezeich":str, "a_lief_einheit":decimal, "a_traubensort":str})
    op_list1_list, Op_list1 = create_model_like(L_op, {"a_lief_einheit":decimal, "a_traubensort":str})

    L_art = Temp_l_artikel
    l_art_list = temp_l_artikel_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, op_list_list, amount, t_amount, price, description, l_bestand, h_rezlin, l_op, l_artikel
        nonlocal l_art


        nonlocal t_l_bestand, t_h_rezlin, temp_l_artikel, op_list, op_list1, l_art
        nonlocal t_l_bestand_list, t_h_rezlin_list, temp_l_artikel_list, op_list_list, op_list1_list
        return {"msg_str": msg_str, "op-list": op_list_list}

    def create_op_list():

        nonlocal msg_str, op_list_list, amount, t_amount, price, description, l_bestand, h_rezlin, l_op, l_artikel
        nonlocal l_art


        nonlocal t_l_bestand, t_h_rezlin, temp_l_artikel, op_list, op_list1, l_art
        nonlocal t_l_bestand_list, t_h_rezlin_list, temp_l_artikel_list, op_list_list, op_list1_list

        anzahl:decimal = 0
        wert:decimal = 0
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
                    op_list.anzahl = op_list1.anzahl
                    op_list.einzelpreis = op_list1.einzelpreis
                    op_list.warenwert = op_list1.warenwert
                    op_list.op_art = op_list1.op_art
                    op_list.herkunftflag = op_list1.herkunftflag
                    op_list.lscheinnr = op_list1.lscheinnr
                    op_list.fuellflag = op_list1.fuellflag
                    op_list.pos = op_list1.pos
                    op_list.a_lief_einheit = op_list1.a_lief_einheit
                    op_list.a_traubensort = op_list1.a_traubensort
                    op_list.fibu = cost_acct
                    op_list.stornogrund = a_bez

            return
        anzahl = qty
        wert = qty * price
        amount = wert
        t_amount = t_amount + wert

        if curr_lager == 0:

            return
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

    def create_op_list1(p_artnr:int, menge:decimal, oh_ok:bool):

        nonlocal msg_str, op_list_list, amount, t_amount, price, description, l_bestand, h_rezlin, l_op, l_artikel
        nonlocal l_art


        nonlocal t_l_bestand, t_h_rezlin, temp_l_artikel, op_list, op_list1, l_art
        nonlocal t_l_bestand_list, t_h_rezlin_list, temp_l_artikel_list, op_list_list, op_list1_list

        stock_oh:decimal = 0
        inh:decimal = 0
        L_art = Temp_l_artikel
        temp_l_artikel_list.clear()
        temp_l_artikel_list = get_output(s_stockout_create_op_list1bl(p_artnr))

        for t_h_rezlin in query(t_h_rezlin_list):
            inh = menge * t_h_rezlin.menge

            if t_h_rezlin.recipe_flag :
                oh_ok = create_op_list1(t_h_rezlin.artnrlager, inh, oh_ok)

                if not oh_ok:

                    return
            else:

                l_art = query(l_art_list, filters=(lambda l_art :l_art.artnr == t_h_rezlin.artnrlager), first=True)

                t_l_bestand = query(t_l_bestand_list, filters=(lambda t_l_bestand :t_l_bestand.lager_nr == curr_lager and t_l_bestand.artnr == t_h_rezlin.artnrlager), first=True)

                if not t_l_bestand:
                    msg_str = "Article " + to_string(l_art.artnr, "9999999") + " - " + l_art.bezeich + " not found, posting not possible."
                    oh_ok = False

                    return
                stock_oh = t_l_bestand.anz_anf_best + t_l_bestand.anz_eingang - t_l_bestand.anz_ausgang
                inh = inh / l_art.inhalt

                if inh > stock_oh:
                    msg_str = "Quantity over stock_onhand: " + to_string(l_art.artnr, "9999999") + " - " + l_art.bezeich + " " + to_string(inh) + " > " + to_string(stock_oh) + ", posting not possible."
                    oh_ok = False

                    return
                amount = inh * l_art.vk_preis / (1 - t_h_rezlin.lostfact / 100)
                t_amount = t_amount + amount
                op_list1 = Op_list1()
                op_list1_list.append(op_list1)

                op_list1.datum = transdate
                op_list1.lager_nr = curr_lager
                op_list1.artnr = l_art.artnr
                op_list1.zeit = get_current_time_in_seconds()
                op_list1.anzahl = inh
                op_list1.einzelpreis = l_art.vk_preis
                op_list1.warenwert = amount
                op_list1.op_art = 3
                op_list1.herkunftflag = 1
                op_list1.lscheinnr = lscheinnr
                op_list1.fuellflag = tp_bediener_nr
                op_list1.pos = 1
                op_list1.a_lief_einheit = l_art.lief_einheit
                op_list1.a_traubensort = l_art.traubensort

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if l_artikel:
        description = l_artikel.bezeich + " - " + l_artikel.masseinheit
        price = l_artikel.vk_preis


        create_op_list()

    return generate_output()