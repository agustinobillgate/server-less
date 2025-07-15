#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, Parameters, L_lager, L_artikel, L_bestand, Gl_acct

def chg_storerequest_read_databl(t_lschein:string, t_datum:date, t_amount:Decimal, lscheinnr:string):

    prepare_cache ([Bediener, Parameters, L_lager, L_artikel, L_bestand, Gl_acct])

    curr_lager = 0
    deptno = 0
    transfered = False
    out_type = 0
    to_stock = 0
    deptname = ""
    lager_bezeich = ""
    lager_bez1 = ""
    curr_pos = 0
    op_list_data = []
    l_op = bediener = parameters = l_lager = l_artikel = l_bestand = gl_acct = None

    op_list = sys_user = None

    op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "anzahl0":Decimal, "fibu":string, "fibu10":string, "s_recid":int, "einheit":string})

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_lager, deptno, transfered, out_type, to_stock, deptname, lager_bezeich, lager_bez1, curr_pos, op_list_data, l_op, bediener, parameters, l_lager, l_artikel, l_bestand, gl_acct
        nonlocal t_lschein, t_datum, t_amount, lscheinnr
        nonlocal sys_user


        nonlocal op_list, sys_user
        nonlocal op_list_data

        return {"t_amount": t_amount, "lscheinnr": lscheinnr, "curr_lager": curr_lager, "deptno": deptno, "transfered": transfered, "out_type": out_type, "to_stock": to_stock, "deptname": deptname, "lager_bezeich": lager_bezeich, "lager_bez1": lager_bez1, "curr_pos": curr_pos, "op-list": op_list_data}

    def read_data():

        nonlocal curr_lager, deptno, transfered, out_type, to_stock, deptname, lager_bezeich, lager_bez1, curr_pos, op_list_data, l_op, bediener, parameters, l_lager, l_artikel, l_bestand, gl_acct
        nonlocal t_lschein, t_datum, t_amount, lscheinnr
        nonlocal sys_user


        nonlocal op_list, sys_user
        nonlocal op_list_data


        lscheinnr = t_lschein

        l_op = get_cache (L_op, {"datum": [(eq, t_datum)],"lscheinnr": [(eq, t_lschein)],"pos": [(gt, 0)]})

        if l_op:
            curr_lager = l_op.lager_nr
            deptno = l_op.reorgflag

            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptno)).first()

            if parameters:
                deptname = parameters.vstring

            if l_op.op_art == 14:
                transfered = True
                out_type = 1
                to_stock = l_op.pos


            else:
                out_type = 2

            l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})

            if l_lager:
                lager_bezeich = l_lager.bezeich

            if to_stock != 0:

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, to_stock)]})

                if l_lager:
                    lager_bez1 = l_lager.bezeich

            for l_op in db_session.query(L_op).filter(
                     (L_op.datum == t_datum) & (L_op.lscheinnr == (t_lschein).lower()) & (L_op.pos > 0) & (L_op.loeschflag == 0)).order_by(L_op.pos).all():
                op_list = Op_list()
                op_list_data.append(op_list)

                buffer_copy(l_op, op_list)

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

                if l_artikel:
                    op_list.bezeich = l_artikel.bezeich
                    op_list.einheit = l_artikel.masseinheit

                sys_user = get_cache (Bediener, {"nr": [(eq, l_op.fuellflag)]})

                if sys_user:
                    op_list.username = sys_user.username

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, curr_lager)]})
                op_list.s_recid = to_int(l_op._recid)
                op_list.anzahl0 =  to_decimal(l_op.anzahl)
                op_list.fibu = l_op.stornogrund
                op_list.fibu10 = l_op.stornogrund
                curr_pos = l_op.pos
                t_amount =  to_decimal(t_amount) + to_decimal(l_op.warenwert)

                if l_bestand:
                    op_list.onhand =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if not gl_acct:

                    gl_acct = get_cache (Gl_acct, {"bezeich": [(eq, l_op.stornogrund)]})

                if gl_acct:
                    op_list.fibu = gl_acct.fibukonto
                    op_list.fibu10 = gl_acct.fibukonto
                    op_list.stornogrund = gl_acct.bezeich

    read_data()

    return generate_output()