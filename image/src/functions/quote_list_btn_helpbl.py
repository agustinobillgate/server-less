from functions.additional_functions import *
import decimal
from models import L_artikel

def quote_list_btn_helpbl(pvilanguage:int, curr_select:str, art_no:int):
    art_name = ""
    dev_unit = ""
    cont = 0
    msg_str = ""
    lvcarea:str = "quote_list"
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_name, dev_unit, cont, msg_str, lvcarea, l_artikel


        return {"art_name": art_name, "dev_unit": dev_unit, "cont": cont, "msg_str": msg_str}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == art_no)).first()

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
        dev_unit = l_artikel.traubensort
        cont = l_artikel.lief_einheit

    return generate_output()