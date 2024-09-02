from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Fa_artikel, Mathis

def prepare_select_faartbl(name:str, nr:int):
    q1_list_list = []
    fa_artikel = mathis = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"name":str, "nr":int, "asset":str, "warenwert":decimal, "anzahl":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, fa_artikel, mathis


        nonlocal q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    mathis_obj_list = []
    for mathis, fa_artikel in db_session.query(Mathis, Fa_artikel).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0) &  (Fa_artikel.warenwert > 0) &  (Fa_artikel.depn_wert == 0)).filter(
            (func.lower(Mathis.(name).lower()) >= (name).lower()) &  (Mathis.flag == 2) &  (Mathis.nr != nr)).all():
        if mathis._recid in mathis_obj_list:
            continue
        else:
            mathis_obj_list.append(mathis._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.name = mathis.name
        q1_list.nr = mathis.nr
        q1_list.asset = mathis.asset
        q1_list.warenwert = fa_artikel.warenwert
        q1_list.anzahl = fa_artikel.anzahl

    return generate_output()