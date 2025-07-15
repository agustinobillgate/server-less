#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_kateg

def prepare_select_fakategbl():

    prepare_cache ([Fa_kateg])

    q1_list_data = []
    fa_kateg = None

    q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"katnr":int, "bezeich":string, "rate":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, fa_kateg


        nonlocal q1_list
        nonlocal q1_list_data

        return {"q1-list": q1_list_data}

    for fa_kateg in db_session.query(Fa_kateg).order_by(Fa_kateg.katnr).all():
        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.katnr = fa_kateg.katnr
        q1_list.bezeich = fa_kateg.bezeich
        q1_list.rate =  to_decimal(fa_kateg.rate)

    return generate_output()