from functions.additional_functions import *
import decimal
from models import Mc_types, Mc_disc, Mc_guest

def mc_typeadmin_btn_exitbl(g_list:[G_list], case_type:int, rec_id:int):
    mc_types = mc_disc = mc_guest = None

    g_list = None

    g_list_list, G_list = create_model("G_list")


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mc_types, mc_disc, mc_guest


        nonlocal g_list
        nonlocal g_list_list
        return {}

    g_list = query(g_list_list, first=True)

    if case_type == 1:
        mc_types = Mc_types()
        db_session.add(mc_types)

        buffer_copy(g_list, mc_types)

    elif case_type == 2:

        mc_types = db_session.query(Mc_types).filter(
                (Mc_types._recid == rec_id)).first()

        if mc_types.nr != g_list.nr:

            for mc_disc in db_session.query(Mc_disc).filter(
                    (Mc_disc.nr == mc_type.nr)).all():
                mc_disc.nr = g_list.nr

            for mc_guest in db_session.query(Mc_guest).filter(
                    (Mc_guest.nr == mc_type.nr)).all():
                mc_guest.nr = g_list.nr
        buffer_copy(g_list, mc_types)

    return generate_output()