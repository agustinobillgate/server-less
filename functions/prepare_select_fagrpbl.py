#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_grup

def prepare_select_fagrpbl():

    prepare_cache ([Fa_grup])

    q1_list_data = []
    fa_grup = None

    q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"gnr":int, "bezeich":string, "flag":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, fa_grup


        nonlocal q1_list
        nonlocal q1_list_data

        return {"q1-list": q1_list_data}

    for fa_grup in db_session.query(Fa_grup).filter(
             (Fa_grup.flag == 0)).order_by(Fa_grup.gnr).all():
        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.gnr = fa_grup.gnr
        q1_list.bezeich = fa_grup.bezeich
        q1_list.flag = fa_grup.flag

    return generate_output()