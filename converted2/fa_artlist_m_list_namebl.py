#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis

def fa_artlist_m_list_namebl(m_list_name:string):

    prepare_cache ([Mathis])

    mathis1_model = ""
    avail_mathis1 = False
    mathis = None

    mathis1 = None

    Mathis1 = create_buffer("Mathis1",Mathis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis1_model, avail_mathis1, mathis
        nonlocal m_list_name
        nonlocal mathis1


        nonlocal mathis1

        return {"mathis1_model": mathis1_model, "avail_mathis1": avail_mathis1}


    mathis1 = get_cache (Mathis, {"name": [(eq, m_list_name)]})

    if mathis1:
        avail_mathis1 = True
        mathis1_model = mathis1.model

    return generate_output()