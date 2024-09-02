from functions.additional_functions import *
import decimal
from datetime import date
from models import L_op, Bediener, L_artikel, H_rezlin, L_bestand, Gl_acct

def s_storerequest_create_op_list1bl(pvilanguage:int, p_artnr:int, menge:decimal, oh_ok:bool, curr_lager:int, transdate:date, lscheinnr:str, bediener_nr:int):
    msg_str = ""
    op_list1_list = []
    lvcarea:str = "s_storerequest"
    amount:decimal = 0
    t_amount:decimal = 0
    l_op = bediener = l_artikel = h_rezlin = l_bestand = gl_acct = None

    op_list = op_list1 = sys_user = l_art = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str, "onhand":decimal, "acct_bez":str})
    op_list1_list, Op_list1 = create_model_like(Op_list)

    Sys_user = Bediener
    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, op_list1_list, lvcarea, amount, t_amount, l_op, bediener, l_artikel, h_rezlin, l_bestand, gl_acct
        nonlocal sys_user, l_art


        nonlocal op_list, op_list1, sys_user, l_art
        nonlocal op_list_list, op_list1_list
        return {"msg_str": msg_str, "op-list1": op_list1_list}

    def create_op_list1():

        nonlocal msg_str, op_list1_list, lvcarea, amount, t_amount, l_op, bediener, l_artikel, h_rezlin, l_bestand, gl_acct
        nonlocal sys_user, l_art


        nonlocal op_list, op_list1, sys_user, l_art
        nonlocal op_list_list, op_list1_list

        stock_oh:decimal = 0
        inh:decimal = 0
        L_art = L_artikel

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():
            inh = menge * h_rezlin.menge

            if h_rezlin.recipe_flag :
                create_op_list1(h_rezlin.artnrlager, inh)
            else:

                l_art = db_session.query(L_art).filter(
                        (L_art.artnr == h_rezlin.artnrlager)).first()

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == h_rezlin.artnrlager)).first()

                if not l_bestand:
                    msg_str = msg_str + chr(2) + translateExtended ("Article ", lvcarea, "") + to_string(l_art.artnr, "9999999") + " - " + l_art.bezeich + " not found, posting not possible."
                    oh_ok = False

                    return
                stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
                inh = inh / l_art.inhalt

                if inh > stock_oh:
                    msg_str = msg_str + chr(2) + translateExtended ("Quantity over stock_onhand: ", lvcarea, "") + to_string(l_art.artnr, "9999999") + " - " + l_art.bezeich + chr(10) + "  (" + to_string(inh) + " > " + to_string(stock_oh) + translateExtended ("), posting not possible.", lvcarea, "")
                    oh_ok = False

                    return
                amount = inh * l_art.vk_preis / (1 - h_rezlin.lostfact / 100)
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
                op_list1.op_art = 13
                op_list1.herkunftflag = 1
                op_list1.lscheinnr = lscheinnr
                op_list1.fuellflag = bediener_nr
                op_list1.pos = 1

                l_art = db_session.query(L_art).filter(
                        (L_art.artnr == op_list1.artnr)).first()

                sys_user = db_session.query(Sys_user).filter(
                        (Sys_user.nr == op_list1.fuellflag)).first()

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == op_list1.artnr) &  (L_bestand.lager_nr == curr_lager)).first()
                op_list1.bezeich = l_art.bezeich
                op_list1.username = sys_user.username

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == op_list1.stornogrund)).first()

                if gl_acct:
                    op_list1.acct_bez = gl_acct.bezeich

                if l_bestand:
                    op_list1.onhand = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

    create_op_list1()

    return generate_output()