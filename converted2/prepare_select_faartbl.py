#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_artikel, Mathis

def prepare_select_faartbl(name:string, nr:int):

    prepare_cache ([Fa_artikel, Mathis])

    q1_list_data = []
    fa_artikel = mathis = None

    q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"name":string, "nr":int, "asset":string, "warenwert":Decimal, "anzahl":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, fa_artikel, mathis
        nonlocal name, nr


        nonlocal q1_list
        nonlocal q1_list_data

        return {"q1-list": q1_list_data}

    mathis_obj_list = {}
    mathis = Mathis()
    fa_artikel = Fa_artikel()
    for mathis.name, mathis.nr, mathis.asset, mathis._recid, fa_artikel.warenwert, fa_artikel.anzahl, fa_artikel._recid in db_session.query(Mathis.name, Mathis.nr, Mathis.asset, Mathis._recid, Fa_artikel.warenwert, Fa_artikel.anzahl, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.warenwert > 0) & (Fa_artikel.depn_wert == 0)).filter(
             (Mathis.name >= (name).lower()) & (Mathis.flag == 2) & (Mathis.nr != nr)).order_by(Mathis.name, Mathis.asset).all():
        if mathis_obj_list.get(mathis._recid):
            continue
        else:
            mathis_obj_list[mathis._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.name = mathis.name
        q1_list.nr = mathis.nr
        q1_list.asset = mathis.asset
        q1_list.warenwert =  to_decimal(fa_artikel.warenwert)
        q1_list.anzahl = fa_artikel.anzahl

    return generate_output()