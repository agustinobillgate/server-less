#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis, Fa_artikel

def fa_artlist_m_list_name1bl(m_list_name:string):

    prepare_cache ([Mathis, Fa_artikel])

    mathis1_model = ""
    mathis1_supplier = ""
    do_it = False
    fa_model:string = ""
    fa_name:string = ""
    mathis = fa_artikel = None

    mathis1 = None

    Mathis1 = create_buffer("Mathis1",Mathis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis1_model, mathis1_supplier, do_it, fa_model, fa_name, mathis, fa_artikel
        nonlocal m_list_name
        nonlocal mathis1


        nonlocal mathis1

        return {"mathis1_model": mathis1_model, "mathis1_supplier": mathis1_supplier, "do_it": do_it}


    mathis1 = get_cache (Mathis, {"name": [(eq, m_list_name)]})

    if mathis1:

        if mathis1.model == None or trim(mathis1.model) == "":
            fa_model = ""
        else:
            fa_model = mathis1.model + " - "

        if mathis1.name == None:
            fa_name = ""
        else:
            fa_name = mathis1.name
        mathis1_model = fa_model + fa_name
        mathis1_supplier = mathis1.supplier

        fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, mathis1.nr)]})

        if fa_artikel:

            if fa_artikel.loeschflag == 0:
                do_it = True

    return generate_output()