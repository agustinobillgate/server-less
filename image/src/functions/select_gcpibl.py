from functions.additional_functions import *
import decimal
from models import Gc_pitype, Bediener, Gc_pi

def select_gcpibl():
    b1_list_list = []
    gc_pitype = bediener = gc_pi = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"datum":date, "docu_nr":str, "betrag":decimal, "bemerk":str, "username":str, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, gc_pitype, bediener, gc_pi


        nonlocal b1_list
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    gc_pi_obj_list = []
    for gc_pi, gc_pitype, bediener in db_session.query(Gc_pi, Gc_pitype, Bediener).join(Gc_pitype,(Gc_pitype.nr == Gc_pi.pi_type)).join(Bediener,(Bediener.userinit == Gc_pi.rcvID)).filter(
            (Gc_pi.pi_status == 0)).all():
        if gc_pi._recid in gc_pi_obj_list:
            continue
        else:
            gc_pi_obj_list.append(gc_pi._recid)


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.datum = gc_pi.datum
        b1_list.docu_nr = gc_pi.docu_nr
        b1_list.betrag = gc_pi.betrag
        b1_list.bemerk = gc_pi.bemerk
        b1_list.username = bediener.username
        b1_list.bezeich = gc_pitype.bezeich

    return generate_output()