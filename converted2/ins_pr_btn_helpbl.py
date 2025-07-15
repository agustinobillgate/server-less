#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, L_artikel

def ins_pr_btn_helpbl(pvilanguage:int, curr_select:string, acct:string, s_artnr:int):

    prepare_cache ([L_artikel])

    outputchar = ""
    l_traubensort = ""
    l_lief_einheit = to_decimal("0.0")
    msg_str = ""
    lvcarea:string = "ins-pr"
    gl_acct = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outputchar, l_traubensort, l_lief_einheit, msg_str, lvcarea, gl_acct, l_artikel
        nonlocal pvilanguage, curr_select, acct, s_artnr

        return {"outputchar": outputchar, "l_traubensort": l_traubensort, "l_lief_einheit": l_lief_einheit, "msg_str": msg_str}


    if curr_select.lower()  == ("cost-acct").lower() :

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, acct)]})

        if gl_acct:
            outputchar = acct

    elif curr_select.lower()  == ("artnr").lower() :

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

        if l_artikel.betriebsnr != 0:
            msg_str = translateExtended ("This is a special article not for purchasing.", lvcarea, "")

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
        l_traubensort = l_artikel.traubensorte
        l_lief_einheit =  to_decimal(l_artikel.lief_einheit)
        outputchar = trim(l_artikel.bezeich) + " - " +\
                to_string(l_artikel.inhalt) + " " +\
                to_string(l_artikel.masseinheit, "x(3)")

    return generate_output()