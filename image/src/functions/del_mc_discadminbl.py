from functions.additional_functions import *
import decimal
from models import Hoteldpt, Mc_disc

def del_mc_discadminbl(curr_nr:int, rec_id:int):
    hoteldpt = mc_disc = None

    hbuff = None

    Hbuff = Hoteldpt

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hoteldpt, mc_disc
        nonlocal hbuff


        nonlocal hbuff
        return {}


    mc_disc = db_session.query(Mc_disc).filter(
            (Mc_disc.nr == curr_nr) &  (Mc_disc._recid == rec_id)).first()

    if mc_disc:

        mc_disc = db_session.query(Mc_disc).first()
        db_session.delete(mc_disc)


    return generate_output()