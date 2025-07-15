#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rset, Bk_raum, Bk_setup

def prepare_select_setupbl(raum:string):

    prepare_cache ([Bk_rset, Bk_raum, Bk_setup])

    t_setup_data = []
    bk_rset = bk_raum = bk_setup = None

    t_setup = None

    t_setup_data, T_setup = create_model("T_setup", {"room":string, "setup":string, "maxperson":int, "roomspace":int, "preptime":int, "extention":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_setup_data, bk_rset, bk_raum, bk_setup
        nonlocal raum


        nonlocal t_setup
        nonlocal t_setup_data

        return {"t-setup": t_setup_data}

    for bk_rset in db_session.query(Bk_rset).filter(
             (Bk_rset.raum == (raum).lower())).order_by(Bk_rset._recid).all():

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_rset.raum)]})

        if bk_raum:

            bk_setup = get_cache (Bk_setup, {"setup_id": [(eq, bk_rset.setup_id)]})

            if bk_setup:
                t_setup = T_setup()
                t_setup_data.append(t_setup)

                t_setup.room = bk_raum.bezeich
                t_setup.setup = bk_setup.bezeich
                t_setup.maxperson = bk_rset.personen
                t_setup.roomspace = bk_rset.groesse
                t_setup.preptime = bk_rset.vorbereit
                t_setup.extention = bk_rset.nebenstelle

    return generate_output()