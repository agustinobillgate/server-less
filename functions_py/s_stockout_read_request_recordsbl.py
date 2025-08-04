#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Andika 04/08/2025
# gitlab: -
# remarks: -
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_ophdr, Bediener, L_artikel, Gl_acct, L_lager, Queasy

def s_stockout_read_request_recordsbl(rec_id:int, out_type:int, t_lschein:string, t_datum:date, user_init:string, t_amount:Decimal):

    prepare_cache ([L_op, Bediener, L_artikel, Gl_acct, L_lager, Queasy])

    lscheinnr = ""
    cost_acct = ""
    lager_bezeich = ""
    lager_bez1 = ""
    curr_lager = 0
    to_stock = 0
    to_stock_ro = False
    t_l_ophdr_data = []
    op_list_data = []
    l_op = l_ophdr = bediener = l_artikel = gl_acct = l_lager = queasy = None

    op_list = t_l_ophdr = out_list = None

    op_list_data, Op_list = create_model_like(L_op, {"fibu":string, "a_bezeich":string, "a_lief_einheit":Decimal, "a_traubensort":string})
    t_l_ophdr_data, T_l_ophdr = create_model_like(L_ophdr, {"rec_id":int, "sr_remark":string})
    out_list_data, Out_list = create_model("Out_list", {"artnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lscheinnr, cost_acct, lager_bezeich, lager_bez1, curr_lager, to_stock, to_stock_ro, t_l_ophdr_data, op_list_data, l_op, l_ophdr, bediener, l_artikel, gl_acct, l_lager, queasy
        nonlocal rec_id, out_type, t_lschein, t_datum, user_init, t_amount


        nonlocal op_list, t_l_ophdr, out_list
        nonlocal op_list_data, t_l_ophdr_data, out_list_data

        return {"t_amount": t_amount, "lscheinnr": lscheinnr, "cost_acct": cost_acct, "lager_bezeich": lager_bezeich, "lager_bez1": lager_bez1, "curr_lager": curr_lager, "to_stock": to_stock, "to_stock_ro": to_stock_ro, "t-l-ophdr": t_l_ophdr_data, "op-list": op_list_data}

    def read_request_records():

        nonlocal lscheinnr, cost_acct, lager_bezeich, lager_bez1, curr_lager, to_stock, to_stock_ro, t_l_ophdr_data, op_list_data, l_op, l_ophdr, bediener, l_artikel, gl_acct, l_lager, queasy
        nonlocal rec_id, out_type, t_lschein, t_datum, user_init, t_amount


        nonlocal op_list, t_l_ophdr, out_list
        nonlocal op_list_data, t_l_ophdr_data, out_list_data

        op_num:int = 13
        sr_remark:string = ""

        if out_type == 1:
            op_num = 14
        lscheinnr = t_lschein

        for l_op in db_session.query(L_op).filter(
                 (L_op.datum == t_datum) & (L_op.op_art == op_num) & (L_op.lscheinnr == (t_lschein).lower()) & (L_op.loeschflag <= 1)).order_by(L_op.artnr).all():

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

            if not gl_acct:

                gl_acct = get_cache (Gl_acct, {"bezeich": [(eq, l_op.stornogrund)]})
            op_list = Op_list()
            op_list_data.append(op_list)

            curr_lager = l_op.lager_nr
            to_stock = l_op.pos
            op_list.lager_nr = l_op.lager_nr
            op_list.artnr = l_op.artnr
            op_list.zeit = get_current_time_in_seconds()
            op_list.anzahl =  to_decimal(l_op.anzahl)
            op_list.einzelpreis =  to_decimal(l_artikel.vk_preis)
            op_list.warenwert =  to_decimal(l_artikel.vk_preis) * to_decimal(l_op.anzahl)
            op_list.op_art = l_op.op_art - 10
            op_list.herkunftflag = 1
            op_list.lscheinnr = l_op.lscheinnr
            op_list.pos = 1
            op_list.stornogrund = l_op.stornogrund
            op_list.betriebsnr = l_op._recid
            op_list.a_bezeich = l_artikel.bezeich


            t_amount =  to_decimal(t_amount) + to_decimal(op_list.warenwert)

            if bediener:
                op_list.fuellflag = bediener.nr

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
        out_list_data.append(out_list)

        out_list.artnr = l_artikel.artnr

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})

        if l_lager:
            lager_bezeich = l_lager.bezeich

        if out_type == 1:

            l_lager = get_cache (L_lager, {"lager_nr": [(eq, to_stock)]})

            if l_lager:
                lager_bez1 = l_lager.bezeich
            to_stock_ro = True
        pass
        l_ophdr.docu_nr = t_lschein
        l_ophdr.lscheinnr = t_lschein
        l_ophdr.op_typ = "STT"


        pass

        queasy = get_cache (Queasy, {"key": [(eq, 343)],"char1": [(eq, t_lschein)]})

        if queasy:
            sr_remark = queasy.char2
        t_l_ophdr = T_l_ophdr()
        t_l_ophdr_data.append(t_l_ophdr)

        buffer_copy(l_ophdr, t_l_ophdr)
        t_l_ophdr.rec_id = l_ophdr._recid
        t_l_ophdr.sr_remark = sr_remark


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, rec_id)]})
    if l_ophdr:
        read_request_records()

    return generate_output()