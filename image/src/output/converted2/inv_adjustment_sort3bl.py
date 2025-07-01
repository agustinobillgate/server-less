#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_untergrup

def inv_adjustment_sort3bl(cbuff_zwkum:int):

    prepare_cache ([L_untergrup])

    a_bez = ""
    l_untergrup = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_bez, l_untergrup
        nonlocal cbuff_zwkum

        return {"a_bez": a_bez}


    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, cbuff_zwkum)]})
    a_bez = l_untergrup.bezeich

    return generate_output()