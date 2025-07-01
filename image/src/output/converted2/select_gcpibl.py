#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pitype, Bediener, Gc_pi

def select_gcpibl():

    prepare_cache ([Gc_pitype, Bediener, Gc_pi])

    b1_list_list = []
    gc_pitype = bediener = gc_pi = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"datum":date, "docu_nr":string, "betrag":Decimal, "bemerk":string, "username":string, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, gc_pitype, bediener, gc_pi


        nonlocal b1_list
        nonlocal b1_list_list

        return {"b1-list": b1_list_list}

    gc_pi_obj_list = {}
    gc_pi = Gc_pi()
    gc_pitype = Gc_pitype()
    bediener = Bediener()
    for gc_pi.datum, gc_pi.docu_nr, gc_pi.betrag, gc_pi.bemerk, gc_pi._recid, gc_pitype.bezeich, gc_pitype._recid, bediener.username, bediener._recid in db_session.query(Gc_pi.datum, Gc_pi.docu_nr, Gc_pi.betrag, Gc_pi.bemerk, Gc_pi._recid, Gc_pitype.bezeich, Gc_pitype._recid, Bediener.username, Bediener._recid).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).join(Bediener,(Bediener.userinit == Gc_pi.rcvid)).filter(
             (Gc_pi.pi_status == 0)).order_by(Gc_pi.datum, Gc_pi.docu_nr).all():
        if gc_pi_obj_list.get(gc_pi._recid):
            continue
        else:
            gc_pi_obj_list[gc_pi._recid] = True


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.datum = gc_pi.datum
        b1_list.docu_nr = gc_pi.docu_nr
        b1_list.betrag =  to_decimal(gc_pi.betrag)
        b1_list.bemerk = gc_pi.bemerk
        b1_list.username = bediener.username
        b1_list.bezeich = gc_pitype.bezeich

    return generate_output()