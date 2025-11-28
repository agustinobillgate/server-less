#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_func
from sqlalchemy.orm import flag_modified

t_kartentext_data, T_kartentext = create_model("T_kartentext", {"kartentext":string, "curr_i":int})
t_sonstiges_data, T_sonstiges = create_model("T_sonstiges", {"sonstiges":string, "curr_i":int})

def main_fs_assign_page3bl(t_kartentext_data:[T_kartentext], t_sonstiges_data:[T_sonstiges], resnr:int, resline:int):

    prepare_cache ([Bk_func])

    kartentext:List[string] = create_empty_list(8,"")
    sonstiges:List[string] = create_empty_list(4,"")
    bk_func = None

    t_kartentext = t_sonstiges = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kartentext, sonstiges, bk_func
        nonlocal resnr, resline


        nonlocal t_kartentext, t_sonstiges

        return {}


    for t_kartentext in query(t_kartentext_data):
        kartentext[t_kartentext.curr_i - 1] = t_kartentext.kartentext

    for t_sonstiges in query(t_sonstiges_data):
        sonstiges[t_sonstiges.curr_i - 1] = t_sonstiges.sonstiges

    # bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})
    bk_func = db_session.query(Bk_func).filter(
             (Bk_func.veran_nr == resnr) &
             (Bk_func.veran_seite == resline)).with_for_update().first()

    if bk_func:
        pass
        bk_func.kartentext[0] = kartentext[0]
        bk_func.kartentext[1] = kartentext[1]
        bk_func.kartentext[2] = kartentext[2]
        bk_func.kartentext[3] = kartentext[3]
        bk_func.kartentext[4] = kartentext[4]
        bk_func.kartentext[5] = kartentext[5]
        bk_func.kartentext[6] = kartentext[6]
        bk_func.kartentext[7] = kartentext[7]
        bk_func.sonstiges[0] = sonstiges[0]
        bk_func.sonstiges[1] = sonstiges[1]
        bk_func.sonstiges[2] = sonstiges[2]
        bk_func.sonstiges[3] = sonstiges[3]

        flag_modified(bk_func, "kartentext")
        flag_modified(bk_func, "sonstiges")
        pass

    return generate_output()