#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, L_artikel, L_order

ins_list_list, Ins_list = create_model("Ins_list", {"t_recid":int, "artnr":int, "bezeich":string, "anzahl":Decimal, "traubensort":string, "txtnr":int, "lieferdatum":date, "stornogrund":string, "bemerk":string, "quality":string, "jahrgang":int, "new_created":bool, "lief_nr":int, "op_art":int, "docu_nr":string, "bestelldatum":date, "soh":Decimal})

def ins_pr_btn_go_webbl(pos:int, user_init:string, ins_list_list:[Ins_list]):

    prepare_cache ([Bediener, L_artikel, L_order])

    tmp_username:string = ""
    bediener = l_artikel = l_order = None

    ins_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmp_username, bediener, l_artikel, l_order
        nonlocal pos, user_init


        nonlocal ins_list

        return {}

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        tmp_username = bediener.username

    l_artikel_obj_list = {}
    for l_artikel in db_session.query(L_artikel).filter(
             ((L_artikel.artnr.in_(list(set([ins_list.artnr for ins_list in ins_list_list if ins_list.new_created])))))).order_by(L_artikel._recid).all():
        if l_artikel_obj_list.get(l_artikel._recid):
            continue
        else:
            l_artikel_obj_list[l_artikel._recid] = True

        ins_list = query(ins_list_list, (lambda ins_list: (l_artikel.artnr == ins_list.artnr)), first=True)
        pos = pos + 1
        l_order = L_order()
        db_session.add(l_order)

        l_order.docu_nr = ins_list.docu_nr
        l_order.artnr = ins_list.artnr
        l_order.anzahl =  to_decimal(ins_list.anzahl)
        l_order.lieferdatum = ins_list.lieferdatum
        l_order.pos = pos
        l_order.bestelldatum = ins_list.bestelldatum
        l_order.op_art = 1
        l_order.lief_fax[0] = tmp_username
        l_order.lief_fax[2] = l_artikel.traubensorte
        l_order.flag = True
        l_order.besteller = ins_list.bemerk
        l_order.stornogrund = ins_list.stornogrund
        l_order.txtnr = l_artikel.lief_einheit

    return generate_output()