#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Mc_disc

disc_list_data, Disc_list = create_model_like(Mc_disc, {"depart":string, "rec_id":int, "counter":int})

def chg_mc_discadmin_webbl(disc_list_data:[Disc_list], curr_nr:int, curr_mode:string):
    mc_disc = None

    disc_list = None

    db_session = local_storage.db_session
    curr_mode = curr_mode.strip()

    def generate_output():
        nonlocal mc_disc
        nonlocal curr_nr, curr_mode


        nonlocal disc_list

        return {}

    if curr_mode.lower()  == ("add").lower() :

        for disc_list in query(disc_list_data, filters=(lambda disc_list: disc_list.nr == curr_nr)):

            mc_disc = get_cache (Mc_disc, {"nr": [(eq, disc_list.nr)],"_recid": [(eq, disc_list.rec_id)]})

            if not mc_disc:
                mc_disc = Mc_disc()
                db_session.add(mc_disc)

                buffer_copy(disc_list, mc_disc)

    elif curr_mode.lower()  == ("chg").lower() :

        disc_list = query(disc_list_data, first=True)

        if disc_list:

            # mc_disc = get_cache (Mc_disc, {"nr": [(eq, curr_nr)],"_recid": [(eq, disc_list.rec_id)]})
            mc_disc = db_session.query(Mc_disc).filter(
                     (Mc_disc.nr == curr_nr) &
                     (Mc_disc._recid == disc_list.rec_id)).with_for_update().first()

            if mc_disc:
                pass
                buffer_copy(disc_list, mc_disc)
                pass
                pass

    return generate_output()