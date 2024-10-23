from functions.additional_functions import *
import decimal
from models import Hoteldpt, Mc_disc

def del_mc_discadminbl(curr_nr:int, rec_id:int):
    hoteldpt = mc_disc = None

    hbuff = None

    Hbuff = create_buffer("Hbuff",Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hoteldpt, mc_disc
        nonlocal curr_nr, rec_id
        nonlocal hbuff


        nonlocal hbuff
        return {}


    mc_disc = db_session.query(Mc_disc).filter(
             (Mc_disc.nr == curr_nr) & (Mc_disc._recid == rec_id)).first()

    if mc_disc:
        db_session.delete(mc_disc)
        pass

    return generate_output()