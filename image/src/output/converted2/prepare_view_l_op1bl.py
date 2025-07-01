#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Htparam, L_artikel, L_op

def prepare_view_l_op1bl(user_init:string):

    prepare_cache ([Bediener, Htparam, L_artikel, L_op])

    show_price = False
    q1_list_list = []
    q11_list_list = []
    bediener = htparam = l_artikel = l_op = None

    sys_user = q1_list = q11_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":string, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "lscheinnr":string, "username":string, "zeit":int, "stornogrund":string, "pos":int})
    q11_list_list, Q11_list = create_model("Q11_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":string, "anzahl":Decimal, "lscheinnr":string, "username":string, "zeit":int, "stornogrund":string, "pos":int})

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, q1_list_list, q11_list_list, bediener, htparam, l_artikel, l_op
        nonlocal user_init
        nonlocal sys_user


        nonlocal sys_user, q1_list, q11_list
        nonlocal q1_list_list, q11_list_list

        return {"show_price": show_price, "q1-list": q1_list_list, "q11-list": q11_list_list}


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    if show_price:

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        sys_user = Bediener()
        for l_op.datum, l_op.lager_nr, l_op.artnr, l_op.anzahl, l_op.einzelpreis, l_op.warenwert, l_op.lscheinnr, l_op.zeit, l_op.stornogrund, l_op.pos, l_op._recid, l_artikel.bezeich, l_artikel._recid, sys_user.permissions, sys_user._recid, sys_user.username in db_session.query(L_op.datum, L_op.lager_nr, L_op.artnr, L_op.anzahl, L_op.einzelpreis, L_op.warenwert, L_op.lscheinnr, L_op.zeit, L_op.stornogrund, L_op.pos, L_op._recid, L_artikel.bezeich, L_artikel._recid, Sys_user.permissions, Sys_user._recid, Sys_user.username).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(Sys_user,(Sys_user.nr == L_op.fuellflag)).filter(
                 (L_op.docu_nr == docu_nr) & (L_op.pos > 0) & (L_op.loeschflag == 0) & (L_op.op_art == 1)).order_by(L_op.lscheinnr, L_op.pos).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.datum = l_op.datum
            q1_list.lager_nr = l_op.lager_nr
            q1_list.artnr = l_op.artnr
            q1_list.bezeich = l_artikel.bezeich
            q1_list.anzahl =  to_decimal(l_op.anzahl)
            q1_list.einzelpreis =  to_decimal(l_op.einzelpreis)
            q1_list.warenwert =  to_decimal(l_op.warenwert)
            q1_list.lscheinnr = l_op.lscheinnr
            q1_list.username = sys_user.username
            q1_list.zeit = l_op.zeit
            q1_list.stornogrund = l_op.stornogrund
            q1_list.pos = l_op.pos


    else:

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        sys_user = Bediener()
        for l_op.datum, l_op.lager_nr, l_op.artnr, l_op.anzahl, l_op.einzelpreis, l_op.warenwert, l_op.lscheinnr, l_op.zeit, l_op.stornogrund, l_op.pos, l_op._recid, l_artikel.bezeich, l_artikel._recid, sys_user.permissions, sys_user._recid, sys_user.username in db_session.query(L_op.datum, L_op.lager_nr, L_op.artnr, L_op.anzahl, L_op.einzelpreis, L_op.warenwert, L_op.lscheinnr, L_op.zeit, L_op.stornogrund, L_op.pos, L_op._recid, L_artikel.bezeich, L_artikel._recid, Sys_user.permissions, Sys_user._recid, Sys_user.username).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(Sys_user,(Sys_user.nr == L_op.fuellflag)).filter(
                 (L_op.docu_nr == docu_nr) & (L_op.pos > 0) & (L_op.loeschflag == 0) & (L_op.op_art == 1)).order_by(L_op.lscheinnr, L_op.pos).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            q11_list = Q11_list()
            q11_list_list.append(q11_list)

            q11_list.datum = l_op.datum
            q11_list.lager_nr = l_op.lager_nr
            q11_list.artnr = l_op.artnr
            q11_list.bezeich = l_artikel.bezeich
            q11_list.anzahl =  to_decimal(l_op.anzahl)
            q11_list.lscheinnr = l_op.lscheinnr
            q11_list.username = sys_user.username
            q11_list.zeit = l_op.zeit
            q11_list.stornogrund = l_op.stornogrund
            q11_list.pos = l_op.pos

    return generate_output()