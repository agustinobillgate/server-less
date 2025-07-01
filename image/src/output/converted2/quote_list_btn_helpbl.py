#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def quote_list_btn_helpbl(pvilanguage:int, curr_select:string, art_no:int):

    prepare_cache ([L_artikel])

    art_name = ""
    dev_unit = ""
    cont = 0
    msg_str = ""
    lvcarea:string = "quote-list"
    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_name, dev_unit, cont, msg_str, lvcarea, l_artikel
        nonlocal pvilanguage, curr_select, art_no

        return {"art_name": art_name, "dev_unit": dev_unit, "cont": cont, "msg_str": msg_str}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, art_no)]})

    if l_artikel and l_artikel.betriebsnr != 0:
        art_no = 0
        art_name = ""
        dev_unit = ""
        cont = 0
        msg_str = translateExtended ("This is a special article not for purchasing.", lvcarea, "")

    elif l_artikel:
        art_name = trim(l_artikel.bezeich) + " - " +\
                to_string(l_artikel.inhalt) + " " +\
                to_string(l_artikel.masseinheit, "x(3)")
        dev_unit = l_artikel.traubensorte
        cont = l_artikel.lief_einheit

    return generate_output()