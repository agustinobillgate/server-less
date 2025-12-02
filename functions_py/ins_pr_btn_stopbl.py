#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_order
ins_list_data, Ins_list = create_model("Ins_list", {"t_recid":int, "artnr":int, "bezeich":string, "anzahl":Decimal, "traubensort":string, "txtnr":int, "lieferdatum":date, "stornogrund":string, "bemerk":string, "quality":string, "jahrgang":int, "new_created":bool, "lief_nr":int, "op_art":int, "docu_nr":string, "bestelldatum":date})

def ins_pr_btn_stopbl(ins_list_data:[Ins_list]):
    l_order = None

    ins_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order


        nonlocal ins_list

        return {}

    for ins_list in query(ins_list_data, filters=(lambda ins_list: ins_list.new_created)):

        # l_order = get_cache (L_order, {"artnr": [(eq, ins_list.artnr)]})
        l_order = db_session.query(L_order).filter(
                     (L_order.artnr == ins_list.artnr)).with_for_update().first()

        if l_order:
            db_session.delete(l_order)

    return generate_output()