#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_akt_kontbl import read_akt_kontbl
from models import Akt_kont

def slc_aktkont_createwebbl(gastnr:int, gname:string):
    kontnr = 0
    t_akt_kont1_list = []
    curr_gastnr:int = 0
    success_flag:bool = False
    akt_kont = None

    t_akt_kont1 = t_akt_kont = None

    t_akt_kont1_list, T_akt_kont1 = create_model_like(Akt_kont)
    t_akt_kont_list, T_akt_kont = create_model_like(Akt_kont)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kontnr, t_akt_kont1_list, curr_gastnr, success_flag, akt_kont
        nonlocal gastnr, gname


        nonlocal t_akt_kont1, t_akt_kont
        nonlocal t_akt_kont1_list, t_akt_kont_list

        return {"kontnr": kontnr, "t-akt-kont1": t_akt_kont1_list}

    t_akt_kont_list = get_output(read_akt_kontbl(6, gastnr, None, ""))

    t_akt_kont = query(t_akt_kont_list, last=True)

    if t_akt_kont:
        curr_gastnr = t_akt_kont.kontakt_nr + 1
    else:
        curr_gastnr = 1
    t_akt_kont1 = T_akt_kont1()
    t_akt_kont1_list.append(t_akt_kont1)

    t_akt_kont1.gastnr = gastnr
    t_akt_kont1.kontakt_nr = curr_gastnr
    t_akt_kont1.name = gname


    kontnr = t_akt_kont1.kontakt_nr

    return generate_output()