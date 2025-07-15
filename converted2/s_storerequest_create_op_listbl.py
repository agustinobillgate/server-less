#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Bediener, L_bestand, Gl_acct

def s_storerequest_create_op_listbl(op_list_artnr:int, op_list_fuellflag:int, op_list_stornogrund:string, curr_lager:int):

    prepare_cache ([L_artikel, Bediener, L_bestand, Gl_acct])

    s_bezeich = ""
    s_bez2 = ""
    s_username = ""
    s_onhand = to_decimal("0.0")
    l_artikel = bediener = l_bestand = gl_acct = None

    l_art = sys_user = None

    L_art = create_buffer("L_art",L_artikel)
    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_bezeich, s_bez2, s_username, s_onhand, l_artikel, bediener, l_bestand, gl_acct
        nonlocal op_list_artnr, op_list_fuellflag, op_list_stornogrund, curr_lager
        nonlocal l_art, sys_user


        nonlocal l_art, sys_user

        return {"s_bezeich": s_bezeich, "s_bez2": s_bez2, "s_username": s_username, "s_onhand": s_onhand}


    l_art = get_cache (L_artikel, {"artnr": [(eq, op_list_artnr)]})

    sys_user = get_cache (Bediener, {"nr": [(eq, op_list_fuellflag)]})

    l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list_artnr)],"lager_nr": [(eq, curr_lager)]})
    s_bezeich = l_art.bezeich
    s_username = sys_user.username

    if l_bestand:
        s_onhand =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, op_list_stornogrund)]})

    if gl_acct:
        s_bez2 = gl_acct.bezeich

    return generate_output()