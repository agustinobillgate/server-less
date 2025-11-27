#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Mc_types, Mc_disc, Mc_guest

g_list_data, G_list = create_model("G_list")

def mc_typeadmin_btn_exitbl(g_list_data:[G_list], case_type:int, rec_id:int):

    prepare_cache ([Mc_types, Mc_disc, Mc_guest])

    mc_types = mc_disc = mc_guest = None

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mc_types, mc_disc, mc_guest
        nonlocal case_type, rec_id


        nonlocal g_list

        return {}

    g_list = query(g_list_data, first=True)

    if case_type == 1:
        mc_types = Mc_types()
        db_session.add(mc_types)

        buffer_copy(g_list, mc_types)

    elif case_type == 2:

        # mc_types = get_cache (Mc_types, {"_recid": [(eq, rec_id)]})
        mc_types = db_session.query(Mc_types).filter(
                 (Mc_types._recid == rec_id)).with_for_update().first()

        if mc_types.nr != g_list.nr:

            for mc_disc in db_session.query(Mc_disc).filter(
                     (Mc_disc.nr == mc_types.nr)).order_by(Mc_disc._recid).all():
                mc_disc.nr = g_list.nr

            for mc_guest in db_session.query(Mc_guest).filter(
                     (Mc_guest.nr == mc_types.nr)).order_by(Mc_guest._recid).all():
                mc_guest.nr = g_list.nr
        buffer_copy(g_list, mc_types)

    return generate_output()