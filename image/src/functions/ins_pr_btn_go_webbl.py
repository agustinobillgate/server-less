from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, L_artikel, L_order

def ins_pr_btn_go_webbl(pos:int, user_init:str, ins_list:[Ins_list]):
    bediener = l_artikel = l_order = None

    ins_list = None

    ins_list_list, Ins_list = create_model("Ins_list", {"t_recid":int, "artnr":int, "bezeich":str, "anzahl":decimal, "traubensort":str, "txtnr":int, "lieferdatum":date, "stornogrund":str, "bemerk":str, "quality":str, "jahrgang":int, "new_created":bool, "lief_nr":int, "op_art":int, "docu_nr":str, "bestelldatum":date, "soh":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, l_artikel, l_order


        nonlocal ins_list
        nonlocal ins_list_list
        return {}

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    for ins_list in query(ins_list_list, filters=(lambda ins_list :ins_list.new_created)):
        l_artikel = db_session.query(L_artikel).filter((L_artikel.artnr == ins_list.artnr)).first()
        if not l_artikel:
            continue

        pos = pos + 1
        l_order = L_order()
        db_session.add(l_order)

        l_order.docu_nr = ins_list.docu_nr
        l_order.artnr = ins_list.artnr
        l_order.anzahl = ins_list.anzahl
        l_order.lieferdatum = ins_list.lieferdatum
        l_order.pos = pos
        l_order.bestelldatum = ins_list.bestelldatum
        l_order.op_art = 1
        l_order.lief_fax[0] = bediener.username
        l_order.lief_fax[2] = l_artikel.traubensort
        l_order.flag = True
        l_order.besteller = ins_list.bemerk
        l_order.stornogrund = ins_list.stornogrund
        l_order.txtnr = l_artikel.lief_einheit

    return generate_output()