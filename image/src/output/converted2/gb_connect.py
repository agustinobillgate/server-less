#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.disp_message import disp_message

def gb_connect():
    variable = None
    pf_filename:string = ""

    db_session = local_storage.db_session

    def generate_output():
        nonlocal variable, pf_filename

        return {}


    if substring(proversion(), 0, 2) == ("10").lower() :
        pf_filename = "c:\\vhpgb\\config\\vhpgb.pfc"

    elif substring(proversion(), 0, 2) == ("11").lower() :
        pf_filename = "c:\\vhpgb11\\config\\vhpgb.pfc"

    if SEARCH ("c:\\vhpgb\\db\\vhpgb.db") == None:
        vhpgbconnect = None

        return generate_output()

    if not CONNECTED ("vhpgb"):

        if vhpgbConnect == None:
            get_output(disp_message("Connecting to VHPGB DB, please wait..", 2))
        CURRENT_WINDOW:LOAD_MOUSE_POINTER ("wait")
        CONNECT -1 c:\vhpgb\db\vhpgb

        if not CONNECTED ("vhpgb"):
            CONNECT -pf VALUE (pf_filename)

        if not CONNECTED ("vhpgb"):
            pf_filename = "c:\\vhpgb11\\config\\vhpgb.pfc"


            CONNECT -pf VALUE (pf_filename)
        CURRENT_WINDOW:LOAD_MOUSE_POINTER ("arrow")

    return generate_output()