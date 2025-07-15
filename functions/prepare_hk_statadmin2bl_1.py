from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimmer, Htparam

def prepare_hk_statadmin2bl(b_zinr:str):
    from_date = None
    zinr = ""
    zimmer = htparam = None

    room = None

    Room = Zimmer

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, zinr, zimmer, htparam
        nonlocal room


        nonlocal room
        return {"from_date": from_date, "zinr": zinr}


    room = db_session.query(Room).filter(
            (func.lower(Room.zinr) == (b_zinr).lower())).first()
    zinr = room.zinr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    from_date = fdate

    return generate_output()