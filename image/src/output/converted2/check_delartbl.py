from functions.additional_functions import *
import decimal
from models import Guestseg, Guest

def check_delartbl(pvilanguage:int, seg_lsegmcode:int, segmcode:int, bezeich:str):
    msg_str = ""
    lvcarea:str = "check-delart"
    name:str = ""
    guestseg = guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, name, guestseg, guest
        nonlocal pvilanguage, seg_lsegmcode, segmcode, bezeich


        return {"msg_str": msg_str}


    guestseg = db_session.query(Guestseg).filter(
             (Guestseg.segmentcode == segmcode)).first()

    if guestseg:

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == guestseg.gastnr)).first()

        if guest:
            name = guest.name
        msg_str = msg_str + chr(2) + translateExtended ("Segment used by guestname", lvcarea, "") + " " + name
    else:
        msg_str = msg_str + chr(2) + "&Q" + translateExtended ("Do you really want to REMOVE the segment", lvcarea, "") + chr(10) + to_string(segmcode) + " - " + bezeich + " ?"

    return generate_output()