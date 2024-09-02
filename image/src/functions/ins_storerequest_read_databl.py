from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, Bediener, Parameters, L_lager, L_artikel, L_bestand

def ins_storerequest_read_databl(t_datum:date, t_lschein:str):
    curr_lager = 0
    deptno = 0
    deptname = ""
    out_type = 0
    to_stock = 0
    lager_bezeich = ""
    transfered = False
    lager_bez1 = ""
    curr_pos = 0
    t_amount = 0
    op_list_list = []
    l_op = bediener = parameters = l_lager = l_artikel = l_bestand = None

    op_list = sys_user = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str, "onhand":decimal, "new_flag":bool}, {"new_flag": True})

    Sys_user = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_lager, deptno, deptname, out_type, to_stock, lager_bezeich, transfered, lager_bez1, curr_pos, t_amount, op_list_list, l_op, bediener, parameters, l_lager, l_artikel, l_bestand
        nonlocal sys_user


        nonlocal op_list, sys_user
        nonlocal op_list_list
        return {"curr_lager": curr_lager, "deptno": deptno, "deptname": deptname, "out_type": out_type, "to_stock": to_stock, "lager_bezeich": lager_bezeich, "transfered": transfered, "lager_bez1": lager_bez1, "curr_pos": curr_pos, "t_amount": t_amount, "op-list": op_list_list}

    l_op = db_session.query(L_op).filter(
            (L_op.datum == t_datum) &  (func.lower(L_op.lscheinnr) == (t_lschein).lower()) &  (L_op.pos > 0)).first()
    curr_lager = l_op.lager
    deptno = l_op.reorgflag

    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == deptno)).first()

    if parameters:
        deptname = parameters.vstring

    if l_op.op_art == 14:
        transfered = True
        out_type = 1
        to_stock = l_op.pos


    else:
        out_type = 2

    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == curr_lager)).first()
    lager_bezeich = l_lager.bezeich

    if to_stock != 0:

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == to_stock)).first()
        lager_bez1 = l_lager.bezeich

    for l_op in db_session.query(L_op).filter(
            (L_op.datum == t_datum) &  (func.lower(L_op.lscheinnr) == (t_lschein).lower()) &  (L_op.pos > 0) &  (L_op.loeschflag <= 1)).all():
        op_list = Op_list()
        op_list_list.append(op_list)

        buffer_copy(l_op, op_list)

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_op.artnr)).first()

        sys_user = db_session.query(Sys_user).filter(
                (Sys_user.nr == l_op.fuellflag)).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == curr_lager)).first()
        op_list.bezeich = l_artikel.bezeich
        op_list.username = sys_user.username
        op_list.new_flag = False
        curr_pos = l_op.pos
        t_amount = t_amount + l_op.warenwert

        if l_bestand:
            op_list.onhand = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

    return generate_output()