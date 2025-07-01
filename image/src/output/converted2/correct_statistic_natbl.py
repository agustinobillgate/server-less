#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def correct_statistic_natbl(a_char:string):

    prepare_cache ([Nation])

    t_nationnr = 0
    t_bezeich = ""
    nation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nationnr, t_bezeich, nation
        nonlocal a_char

        return {"t_nationnr": t_nationnr, "t_bezeich": t_bezeich}


    nation = get_cache (Nation, {"kurzbez": [(eq, a_char)]})
    t_nationnr = nation.nationnr
    t_bezeich = nation.bezeich

    return generate_output()