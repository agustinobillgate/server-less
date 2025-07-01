#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_setup, Bk_rset

def select_basetup_create_listbl(room:string):

    prepare_cache ([Bk_setup, Bk_rset])

    bk_list_list = []
    bk_setup = bk_rset = None

    bk_list = None

    bk_list_list, Bk_list = create_model("Bk_list", {"setup_id":int, "bezeich":string, "pax":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_list_list, bk_setup, bk_rset
        nonlocal room


        nonlocal bk_list
        nonlocal bk_list_list

        return {"bk-list": bk_list_list}

    for bk_setup in db_session.query(Bk_setup).order_by(Bk_setup.setup_id).all():
        bk_list = Bk_list()
        bk_list_list.append(bk_list)

        bk_list.setup_id = bk_setup.setup_id
        bk_list.bezeich = bk_setup.bezeichnung

        if room != "":

            bk_rset = get_cache (Bk_rset, {"raum": [(eq, room)],"setup_id": [(eq, bk_setup.setup_id)]})

            if bk_rset:
                bk_list.pax = bk_rset.personen

    return generate_output()