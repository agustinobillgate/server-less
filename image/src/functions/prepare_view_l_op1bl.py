from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Htparam, L_artikel, L_op

def prepare_view_l_op1bl(user_init:str):
    show_price = False
    q1_list_list = []
    q11_list_list = []
    bediener = htparam = l_artikel = l_op = None

    sys_user = q1_list = q11_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":str, "anzahl":decimal, "einzelpreis":decimal, "warenwert":decimal, "lscheinnr":str, "username":str, "zeit":int, "stornogrund":str, "pos":int})
    q11_list_list, Q11_list = create_model("Q11_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":str, "anzahl":decimal, "lscheinnr":str, "username":str, "zeit":int, "stornogrund":str, "pos":int})

    Sys_user = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, q1_list_list, q11_list_list, bediener, htparam, l_artikel, l_op
        nonlocal sys_user


        nonlocal sys_user, q1_list, q11_list
        nonlocal q1_list_list, q11_list_list
        return {"show_price": show_price, "q1-list": q1_list_list, "q11-list": q11_list_list}


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    if show_price:

        l_op_obj_list = []
        for l_op, l_artikel, sys_user in db_session.query(L_op, L_artikel, Sys_user).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(Sys_user,(Sys_user.nr == L_op.fuellflag)).filter(
                (L_op.docu_nr == docu_nr) &  (L_op.pos > 0) &  (L_op.loeschflag == 0) &  (L_op.op_art == 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.datum = l_op.datum
            q1_list.lager_nr = l_op.lager_nr
            q1_list.artnr = l_op.artnr
            q1_list.bezeich = l_artikel.bezeich
            q1_list.anzahl = l_op.anzahl
            q1_list.einzelpreis = l_op.einzelpreis
            q1_list.warenwert = l_op.warenwert
            q1_list.lscheinnr = l_op.lscheinnr
            q1_list.username = sys_user.username
            q1_list.zeit = l_op.zeit
            q1_list.stornogrund = l_op.stornogrund
            q1_list.pos = l_op.pos


    else:

        l_op_obj_list = []
        for l_op, l_artikel, sys_user in db_session.query(L_op, L_artikel, Sys_user).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(Sys_user,(Sys_user.nr == L_op.fuellflag)).filter(
                (L_op.docu_nr == docu_nr) &  (L_op.pos > 0) &  (L_op.loeschflag == 0) &  (L_op.op_art == 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            q11_list = Q11_list()
            q11_list_list.append(q11_list)

            q11_list.datum = l_op.datum
            q11_list.lager_nr = l_op.lager_nr
            q11_list.artnr = l_op.artnr
            q11_list.bezeich = l_artikel.bezeich
            q11_list.anzahl = l_op.anzahl
            q11_list.lscheinnr = l_op.lscheinnr
            q11_list.username = sys_user.username
            q11_list.zeit = l_op.zeit
            q11_list.stornogrund = l_op.stornogrund
            q11_list.pos = l_op.pos

    return generate_output()