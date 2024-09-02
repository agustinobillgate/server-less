from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_kredit

def supply_inlist_btn_insartbl(pvilanguage:int, str_list_billdate:date, str_list_lief_nr:int, str_list_docu_nr:str, str_list_lscheinnr:str):
    msg_str = ""
    lvcarea:str = "supply_inlist"
    htparam = l_kredit = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, htparam, l_kredit


        return {"msg_str": msg_str}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 269)).first()

    if htparam.fdate != None and htparam.fdate > str_list_billdate:
        msg_str = msg_str + chr(2) + translateExtended ("The receiving record(s) have been transfered to the G/L.", lvcarea, "") + chr(10) + translateExtended ("Inserting is no longer possible.", lvcarea, "")

        return generate_output()

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit.lief_nr == str_list_lief_nr) &  (func.lower(L_kredit.name) == (str_list_docu_nr).lower()) &  (func.lower(L_kredit.lscheinnr) == (str_list_lscheinnr).lower()) &  (L_kredit.opart >= 1) &  (L_kredit.zahlkonto > 0)).first()

    if l_kredit:
        msg_str = msg_str + chr(2) + translateExtended ("The A/P Payment record found.", lvcarea, "") + chr(10) + translateExtended ("Inserting is no longer possible.", lvcarea, "")

        return generate_output()