#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_disc

disc_list_list, Disc_list = create_model_like(Mc_disc, {"depart":string, "rec_id":int, "counter":int})

def chg_mc_discadmin_webbl(disc_list_list:[Disc_list], curr_nr:int, curr_mode:string):
    mc_disc = None

    disc_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mc_disc
        nonlocal curr_nr, curr_mode


        nonlocal disc_list

        return {}

    if curr_mode.lower()  == ("add").lower() :

        for disc_list in query(disc_list_list, filters=(lambda disc_list: disc_list.nr == curr_nr)):

            mc_disc = get_cache (Mc_disc, {"nr": [(eq, disc_list.nr)],"_recid": [(eq, disc_list.rec_id)]})

            if not mc_disc:
                mc_disc = Mc_disc()
                db_session.add(mc_disc)

                buffer_copy(disc_list, mc_disc)

    elif curr_mode.lower()  == ("chg").lower() :

        disc_list = query(disc_list_list, first=True)

        if disc_list:

            mc_disc = get_cache (Mc_disc, {"nr": [(eq, curr_nr)],"_recid": [(eq, disc_list.rec_id)]})

            if mc_disc:
                pass
                buffer_copy(disc_list, mc_disc)
                pass
                pass

    return generate_output()