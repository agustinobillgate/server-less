from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Mathis, L_lieferant, Htparam, Fa_artikel, Fa_grup

def prepare_fa_stinbl(a_bezeich:str):
    billdate = None
    fa_list_list = []
    lief_list_list = []
    mathis = l_lieferant = htparam = fa_artikel = fa_grup = None

    fa_list = lief_list = None

    fa_list_list, Fa_list = create_model_like(Mathis, {"bezeich":str})
    lief_list_list, Lief_list = create_model_like(L_lieferant)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, fa_list_list, lief_list_list, mathis, l_lieferant, htparam, fa_artikel, fa_grup


        nonlocal fa_list, lief_list
        nonlocal fa_list_list, lief_list_list
        return {"billdate": billdate, "fa-list": fa_list_list, "lief-list": lief_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    mathis_obj_list = []
    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (not Fa_artikel.posted) &  (Fa_artikel.loeschflag == 0) &  (Fa_artikel.next_depn == None)).join(Fa_grup,(Fa_grup.gnr == fa_artikel.gnr) &  (Fa_grup.flag == 0)).filter(
            (func.lower(Mathis.name) >= (a_bezeich).lower())).all():
        if mathis._recid in mathis_obj_list:
            continue
        else:
            mathis_obj_list.append(mathis._recid)


        fa_list = Fa_list()
        fa_list_list.append(fa_list)

        buffer_copy(mathis, fa_list)
        fa_list.bezeich = fa_grup.bezeich

    for l_lieferant in db_session.query(L_lieferant).all():
        lief_list = Lief_list()
        lief_list_list.append(lief_list)

        buffer_copy(l_lieferant, lief_list)

    return generate_output()