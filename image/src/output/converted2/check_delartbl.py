#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guestseg, Guest

def check_delartbl(pvilanguage:int, seg_lsegmcode:int, segmcode:int, bezeich:string):

    prepare_cache ([Guestseg, Guest])

    msg_str = ""
    lvcarea:string = "check-delart"
    name:string = ""
    guestseg = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, name, guestseg, guest
        nonlocal pvilanguage, seg_lsegmcode, segmcode, bezeich

        return {"msg_str": msg_str}


    guestseg = get_cache (Guestseg, {"segmentcode": [(eq, segmcode)]})

    if guestseg:

        guest = get_cache (Guest, {"gastnr": [(eq, guestseg.gastnr)]})

        if guest:
            name = guest.name
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Segment used by guestname", lvcarea, "") + " " + name
    else:
        msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("Do you really want to REMOVE the segment", lvcarea, "") + chr_unicode(10) + to_string(segmcode) + " - " + bezeich + " ?"

    return generate_output()