#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mathis, Fa_artikel

def fa_upgradelist_btn_gobl(fdate:date, tdate:date):

    prepare_cache ([Mathis, Fa_artikel])

    q1_list_data = []
    mathis = fa_artikel = None

    mat_buff = q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"mathis_name":string, "mathis_asset":string, "location":string, "warenwert":Decimal, "nr":int, "matbuff_name":string, "matbuff_asset":string, "deleted":date, "did":string, "recid_fa_artikel":int})

    Mat_buff = create_buffer("Mat_buff",Mathis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, mathis, fa_artikel
        nonlocal fdate, tdate
        nonlocal mat_buff


        nonlocal mat_buff, q1_list
        nonlocal q1_list_data

        return {"q1-list": q1_list_data}

    fa_artikel_obj_list = {}
    fa_artikel = Fa_artikel()
    mathis = Mathis()
    mat_buff = Mathis()
    for fa_artikel.warenwert, fa_artikel.deleted, fa_artikel.did, fa_artikel._recid, mathis.name, mathis.asset, mathis.location, mathis._recid, mathis.nr, mat_buff.name, mat_buff.asset, mat_buff.location, mat_buff._recid, mat_buff.nr in db_session.query(Fa_artikel.warenwert, Fa_artikel.deleted, Fa_artikel.did, Fa_artikel._recid, Mathis.name, Mathis.asset, Mathis.location, Mathis._recid, Mathis.nr, Mat_buff.name, Mat_buff.asset, Mat_buff.location, Mat_buff._recid, Mat_buff.nr).join(Mathis,(Mathis.nr == Fa_artikel.nr) & (Mathis.flag == 2)).join(Mat_buff,(Mat_buff.nr == Fa_artikel.p_nr)).filter(
             (Fa_artikel.deleted >= fdate) & (Fa_artikel.deleted <= tdate)).order_by(Fa_artikel.deleted).all():
        if fa_artikel_obj_list.get(fa_artikel._recid):
            continue
        else:
            fa_artikel_obj_list[fa_artikel._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.mathis_name = mathis.name
        q1_list.mathis_asset = mathis.asset
        q1_list.location = mathis.location
        q1_list.warenwert =  to_decimal(fa_artikel.warenwert)
        q1_list.nr = mat_buff.nr
        q1_list.matbuff_name = mat_buff.name
        q1_list.matbuff_asset = mat_buff.asset
        q1_list.deleted = fa_artikel.deleted
        q1_list.did = fa_artikel.did
        q1_list.recid_fa_artikel = fa_artikel._recid

    return generate_output()