from functions.additional_functions import *
import decimal
from models import Mc_disc, Mc_types

def mc_typeadmin_btn_delnamebl(nr:int, rec_id:int):
    mc_disc = mc_types = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mc_disc, mc_types


        return {}


    for mc_disc in db_session.query(Mc_disc).filter(
            (Mc_disc.nr == nr)).all():
        db_session.delete(mc_disc)

    mc_types = db_session.query(Mc_types).filter(
            (Mc_types._recid == rec_id)).first()
    db_session.delete(mc_types)

    return generate_output()