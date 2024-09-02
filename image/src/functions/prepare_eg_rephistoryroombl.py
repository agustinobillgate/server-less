from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimmer, Htparam, Bediener

def prepare_eg_rephistoryroombl(user_init:str):
    ci_date = None
    engid = 0
    groupid = 0
    t_zimmer_list = []
    zimmer = htparam = bediener = None

    t_zimmer = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, engid, groupid, t_zimmer_list, zimmer, htparam, bediener


        nonlocal t_zimmer
        nonlocal t_zimmer_list
        return {"ci_date": ci_date, "engid": engid, "groupid": groupid, "t-zimmer": t_zimmer_list}

    def define_engineering():

        nonlocal ci_date, engid, groupid, t_zimmer_list, zimmer, htparam, bediener


        nonlocal t_zimmer
        nonlocal t_zimmer_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal ci_date, engid, groupid, t_zimmer_list, zimmer, htparam, bediener


        nonlocal t_zimmer
        nonlocal t_zimmer_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    define_group()
    define_engineering()

    for zimmer in db_session.query(Zimmer).all():
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    return generate_output()