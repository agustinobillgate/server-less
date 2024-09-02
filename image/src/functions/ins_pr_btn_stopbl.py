from functions.additional_functions import *
import decimal
from models import L_order

def ins_pr_btn_stopbl(ins_list:[Ins_list]):
    l_order = None

    ins_list = None

    ins_list_list, Ins_list = create_model("Ins_list", {"t_recid":int, "artnr":int, "bezeich":str, "anzahl":decimal, "traubensort":str, "txtnr":int, "lieferdatum":date, "stornogrund":str, "bemerk":str, "quality":str, "jahrgang":int, "new_created":bool, "lief_nr":int, "op_art":int, "docu_nr":str, "bestelldatum":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order


        nonlocal ins_list
        nonlocal ins_list_list
        return {}

    for ins_list in query(ins_list_list, filters=(lambda ins_list :ins_list.new_created)):

        l_order = db_session.query(L_order).filter(
                (L_order.artnr == ins_list.artnr)).first()

        if l_order:
            db_session.delete(l_order)

    return generate_output()