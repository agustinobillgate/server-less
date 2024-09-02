from functions.additional_functions import *
import decimal
from models import Fa_grup

def prepare_select_fasubgrpbl():
    q1_list_list = []
    fa_grup = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"gnr":int, "bezeich":str, "flag":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, fa_grup


        nonlocal q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    for fa_grup in db_session.query(Fa_grup).filter(
            (Fa_grup.flag > 0)).all():
        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.gnr = fa_grup.gnr
        q1_list.bezeich = fa_grup.bezeich
        q1_list.flag = fa_grup.flag

    return generate_output()