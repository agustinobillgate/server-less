from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Mathis, Fa_artikel

def fa_artlist_m_list_name1bl(m_list_name:str):
    mathis1_model = ""
    mathis1_supplier = ""
    do_it = False
    mathis = fa_artikel = None

    mathis1 = None

    Mathis1 = Mathis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis1_model, mathis1_supplier, do_it, mathis, fa_artikel
        nonlocal mathis1


        nonlocal mathis1
        return {"mathis1_model": mathis1_model, "mathis1_supplier": mathis1_supplier, "do_it": do_it}


    mathis1 = db_session.query(Mathis1).filter(
            (func.lower(Mathis1.name) == (m_list_name).lower())).first()

    if mathis1:

        fa_artikel = db_session.query(Fa_artikel).filter(
                (Fa_artikel.nr == mathis1.nr)).first()

        if fa_artikel.loeschflag == 0:
            mathis1_model = mathis1.model
            mathis1_supplier = mathis1.supplier
            do_it = True

    return generate_output()