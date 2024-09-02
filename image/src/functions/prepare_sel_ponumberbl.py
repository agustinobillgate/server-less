from functions.additional_functions import *
import decimal
from models import L_order, L_orderhdr

def prepare_sel_ponumberbl(lief_nr:int, currno:int):
    ponumber_list_list = []
    l_order = l_orderhdr = None

    ponumber_list = None

    ponumber_list_list, Ponumber_list = create_model("Ponumber_list", {"docu_nr":str, "bestelldatum":date, "lieferdatum":date, "lief_fax":[str]})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ponumber_list_list, l_order, l_orderhdr


        nonlocal ponumber_list
        nonlocal ponumber_list_list
        return {"ponumber-list": ponumber_list_list}

    l_orderhdr_obj_list = []
    for l_orderhdr, l_order in db_session.query(L_orderhdr, L_order).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) &  (L_order.loeschflag == 0) &  (L_order.pos == 0) &  ((L_order.angebot_lief[2] == currno) |  (L_order.angebot_lief[2] == 0))).filter(
            (L_orderhdr.lief_nr == lief_nr) &  ((L_orderhdr.angebot_lief[2] == currno) |  (L_orderhdr.angebot_lief[2] == 0)) &  (L_orderhdr.gedruckt == None)).all():
        if l_orderhdr._recid in l_orderhdr_obj_list:
            continue
        else:
            l_orderhdr_obj_list.append(l_orderhdr._recid)


        ponumber_list = Ponumber_list()
        ponumber_list_list.append(ponumber_list)

        ponumber_list.docu_nr = l_orderhdr.docu_nr
        ponumber_list.bestelldatum = l_orderhdr.bestelldatum
        ponumber_list.lieferdatum = l_orderhdr.lieferdatum
        ponumber_list.lief_fax[0] = l_order.lief_fax[0]

    return generate_output()