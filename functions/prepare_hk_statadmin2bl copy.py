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

    Room = create_buffer("Room",Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, zinr, zimmer, htparam
        nonlocal b_zinr
        nonlocal room


        nonlocal room
        return {"from_date": from_date, "zinr": zinr}


    if not room or not(room.zinr.lower()  == (b_zinr).lower()):
        room = db_session.query(Room).filter(
            (func.lower(Room.zinr) == (b_zinr).lower())).first()
    zinr = room.zinr

    if not htparam or not(htparam.paramnr == 87):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    from_date = htparam.fdate

    return generate_output()