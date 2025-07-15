#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_lager

def prepare_select_fastorebl():

    prepare_cache ([Fa_lager])

    q1_list_data = []
    fa_lager = None

    q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"lager_nr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, fa_lager


        nonlocal q1_list
        nonlocal q1_list_data

        return {"q1-list": q1_list_data}

    for fa_lager in db_session.query(Fa_lager).order_by(Fa_lager.lager_nr).all():
        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.lager_nr = fa_lager.lager_nr
        q1_list.bezeich = fa_lager.bezeich

    return generate_output()