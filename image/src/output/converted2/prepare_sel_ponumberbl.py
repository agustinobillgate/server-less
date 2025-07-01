#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_order, L_orderhdr

def prepare_sel_ponumberbl(lief_nr:int, currno:int):

    prepare_cache ([L_order, L_orderhdr])

    ponumber_list_list = []
    l_order = l_orderhdr = None

    ponumber_list = None

    ponumber_list_list, Ponumber_list = create_model("Ponumber_list", {"docu_nr":string, "bestelldatum":date, "lieferdatum":date, "lief_fax":[string,3]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ponumber_list_list, l_order, l_orderhdr
        nonlocal lief_nr, currno


        nonlocal ponumber_list
        nonlocal ponumber_list_list

        return {"ponumber-list": ponumber_list_list}

    l_orderhdr_obj_list = {}
    l_orderhdr = L_orderhdr()
    l_order = L_order()
    for l_orderhdr.docu_nr, l_orderhdr.bestelldatum, l_orderhdr.lieferdatum, l_orderhdr._recid, l_order.lief_fax, l_order._recid in db_session.query(L_orderhdr.docu_nr, L_orderhdr.bestelldatum, L_orderhdr.lieferdatum, L_orderhdr._recid, L_order.lief_fax, L_order._recid).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) & (L_order.loeschflag == 0) & (L_order.pos == 0) & ((L_order.angebot_lief[inc_value(2)] == currno) | (L_order.angebot_lief[inc_value(2)] == 0))).filter(
             (L_orderhdr.lief_nr == lief_nr) & ((L_orderhdr.angebot_lief[inc_value(2)] == currno) | (L_orderhdr.angebot_lief[inc_value(2)] == 0)) & (L_orderhdr.gedruckt == None)).order_by(L_orderhdr.docu_nr).all():
        if l_orderhdr_obj_list.get(l_orderhdr._recid):
            continue
        else:
            l_orderhdr_obj_list[l_orderhdr._recid] = True


        ponumber_list = Ponumber_list()
        ponumber_list_list.append(ponumber_list)

        ponumber_list.docu_nr = l_orderhdr.docu_nr
        ponumber_list.bestelldatum = l_orderhdr.bestelldatum
        ponumber_list.lieferdatum = l_orderhdr.lieferdatum
        ponumber_list.lief_fax[0] = l_order.lief_fax[0]

    return generate_output()