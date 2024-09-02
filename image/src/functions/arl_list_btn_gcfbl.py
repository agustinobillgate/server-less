from functions.additional_functions import *
import decimal
from models import Guest

def arl_list_btn_gcfbl(t_gastnrmember:int, ext_char:str):
    progname = ""
    t_gastnr = 0
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal progname, t_gastnr, guest


        return {"progname": progname, "t_gastnr": t_gastnr}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == t_gastnrmember)).first()
    progname = "chg_gcf" + ext_char + to_string(guest.karteityp) + "UI.p"
    t_gastnr = guest.gastnr

    return generate_output()