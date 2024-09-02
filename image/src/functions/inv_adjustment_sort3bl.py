from functions.additional_functions import *
import decimal
from models import L_untergrup

def inv_adjustment_sort3bl(cbuff_zwkum:int):
    a_bez = ""
    l_untergrup = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_bez, l_untergrup


        return {"a_bez": a_bez}


    l_untergrup = db_session.query(L_untergrup).filter(
            (L_untergrup.zwkum == cbuff_zwkum)).first()
    a_bez = l_untergrup.bezeich

    return generate_output()