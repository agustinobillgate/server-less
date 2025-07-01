#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def subnation_admin_checkbl(pvilanguage:int, kurzbez:string, natcode:int):
    msg_str = ""
    lvcarea:string = "subnation-admin-check"
    nation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, nation
        nonlocal pvilanguage, kurzbez, natcode

        return {"msg_str": msg_str}


    nation = get_cache (Nation, {"kurzbez": [(eq, kurzbez)],"natcode": [(eq, natcode)]})

    if nation and kurzbez != "":
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Region Code already exists, use other code.", lvcarea, "")

        return generate_output()

    nation = get_cache (Nation, {"kurzbez": [(eq, kurzbez)],"natcode": [(eq, 0)]})

    if nation and kurzbez != "":
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Region Code used for a Nation Code, use other code.", lvcarea, "")

        return generate_output()

    return generate_output()