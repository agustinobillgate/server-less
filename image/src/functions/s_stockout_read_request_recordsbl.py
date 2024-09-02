from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_ophdr, Bediener, L_artikel, Gl_acct, L_lager

def s_stockout_read_request_recordsbl(rec_id:int, out_type:int, t_lschein:str, t_datum:date, user_init:str, t_amount:decimal):
    lscheinnr = ""
    cost_acct = ""
    lager_bezeich = ""
    lager_bez1 = ""
    curr_lager = 0
    to_stock = 0
    to_stock_ro = False
    t_l_ophdr_list = []
    op_list_list = []
    l_op = l_ophdr = bediener = l_artikel = gl_acct = l_lager = None

    op_list = t_l_ophdr = out_list = None

    op_list_list, Op_list = create_model_like(L_op, {"fibu":str, "a_bezeich":str, "a_lief_einheit":decimal, "a_traubensort":str})
    t_l_ophdr_list, T_l_ophdr = create_model_like(L_ophdr, {"rec_id":int})
    out_list_list, Out_list = create_model("Out_list", {"artnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lscheinnr, cost_acct, lager_bezeich, lager_bez1, curr_lager, to_stock, to_stock_ro, t_l_ophdr_list, op_list_list, l_op, l_ophdr, bediener, l_artikel, gl_acct, l_lager


        nonlocal op_list, t_l_ophdr, out_list
        nonlocal op_list_list, t_l_ophdr_list, out_list_list
        return {"lscheinnr": lscheinnr, "cost_acct": cost_acct, "lager_bezeich": lager_bezeich, "lager_bez1": lager_bez1, "curr_lager": curr_lager, "to_stock": to_stock, "to_stock_ro": to_stock_ro, "t-l-ophdr": t_l_ophdr_list, "op-list": op_list_list}

    def read_request_records():

        nonlocal lscheinnr, cost_acct, lager_bezeich, lager_bez1, curr_lager, to_stock, to_stock_ro, t_l_ophdr_list, op_list_list, l_op, l_ophdr, bediener, l_artikel, gl_acct, l_lager


        nonlocal op_list, t_l_ophdr, out_list
        nonlocal op_list_list, t_l_ophdr_list, out_list_list

        op_num:int = 13

        if out_type == 1:
            op_num = 14
        lscheinnr = t_lschein

        for l_op in db_session.query(L_op).filter(
                (L_op.datum == t_datum) &  (L_op.op_art == op_num) &  (func.lower(L_op.lscheinnr) == (t_lschein).lower()) &  (L_op.loeschflag <= 1)).all():

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_op.artnr)).first()

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_op.stornogrund)).first()

            if not gl_acct:

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.bezeich == l_op.stornogrund)).first()
            op_list = Op_list()
            op_list_list.append(op_list)

            curr_lager = l_op.lager_nr
            to_stock = l_op.pos
            op_list.lager_nr = l_op.lager_nr
            op_list.artnr = l_op.artnr
            op_list.zeit = get_current_time_in_seconds()
            op_list.anzahl = l_op.anzahl
            op_list.einzelpreis = l_artikel.vk_preis
            op_list.warenwert = l_artikel.vk_preis * l_op.anzahl
            op_list.op_art = l_op.op_art - 10
            op_list.herkunftflag = 1
            op_list.lscheinnr = l_op.lscheinnr
            op_list.fuellflag = bediener.nr
            op_list.pos = 1
            op_list.stornogrund = l_op.stornogrund
            op_list.betriebsnr = l_op._recid
            op_list.a_bezeich = l_artikel.bezeich


            t_amount = t_amount + op_list.warenwert

            if out_type == 2:

                if gl_acct:
                    cost_acct = gl_acct.fibukonto
                else:
                    cost_acct = l_op.stornogrund

            if gl_acct:
                op_list.stornogrund = gl_acct.bezeich
                op_list.fibu = gl_acct.fibukonto

        if out_type == 2:
            to_stock = 0
        out_list = Out_list()
        out_list_list.append(out_list)

        out_list.artnr = l_artikel.artnr

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == curr_lager)).first()

        if l_lager:
            lager_bezeich = l_lager.bezeich

        if out_type == 1:

            l_lager = db_session.query(L_lager).filter(
                    (L_lager.lager_nr == to_stock)).first()

            if l_lager:
                lager_bez1 = l_lager.bezeich
            to_stock_ro = True

        l_ophdr = db_session.query(L_ophdr).first()
        l_ophdr.docu_nr = t_lschein
        l_ophdr.lscheinnr = t_lschein
        l_ophdr.op_typ = "STT"

        l_ophdr = db_session.query(L_ophdr).first()
        t_l_ophdr = T_l_ophdr()
        t_l_ophdr_list.append(t_l_ophdr)

        buffer_copy(l_ophdr, t_l_ophdr)
        t_l_ophdr.rec_id = l_ophdr._recid


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == rec_id)).first()
    read_request_records()

    return generate_output()