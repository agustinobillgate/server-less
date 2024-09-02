from functions.additional_functions import *
import decimal
from models import Fa_kateg

def prepare_select_fakategbl():
    q1_list_list = []
    fa_kateg = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"katnr":int, "bezeich":str, "rate":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, fa_kateg


        nonlocal q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    for fa_kateg in db_session.query(Fa_kateg).all():
        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.katnr = fa_kateg.katnr
        q1_list.bezeich = fa_kateg.bezeich
        q1_list.rate = fa_kateg.rate

    return generate_output()