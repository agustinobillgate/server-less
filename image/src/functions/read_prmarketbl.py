from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Prmarket

def read_prmarketbl(case_type:int, prno:int, bezeich:str):
    t_prmarket_list = []
    prmarket = None

    t_prmarket = None

    t_prmarket_list, T_prmarket = create_model_like(Prmarket)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_prmarket_list, prmarket


        nonlocal t_prmarket
        nonlocal t_prmarket_list
        return {"t-prmarket": t_prmarket_list}

    if case_type == 1:

        prmarket = db_session.query(Prmarket).filter(
                (Prmarket.nr == prno)).first()
    elif case_type == 2:

        prmarket = db_session.query(Prmarket).filter(
                (func.lower(Prmarket.(bezeich).lower()) == (bezeich).lower())).first()
    elif case_type == 3:

        prmarket = db_session.query(Prmarket).filter(
                (func.lower(Prmarket.(bezeich).lower()) == (bezeich).lower()) &  (Prmarket._recid != prno)).first()

    if prmarket:
        t_prmarket = T_prmarket()
        t_prmarket_list.append(t_prmarket)

        buffer_copy(prmarket, t_prmarket)

    return generate_output()