from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Katpreis, Arrangement

def rmcat_rate_btn_gobl(p_list:[P_list], case_type:int, curr_arg:str, rec_id:int):
    katpreis = arrangement = None

    p_list = arr = None

    p_list_list, P_list = create_model_like(Katpreis)

    Arr = Arrangement

    db_session = local_storage.db_session

    def generate_output():
        nonlocal katpreis, arrangement
        nonlocal arr


        nonlocal p_list, arr
        nonlocal p_list_list
        return {}

    def fill_katpreis():

        nonlocal katpreis, arrangement
        nonlocal arr


        nonlocal p_list, arr
        nonlocal p_list_list


        Arr = Arrangement

        arr = db_session.query(Arr).filter(
                (func.lower(Arr.arrangement) == (curr_arg).lower())).first()
        katpreis.zikatnr = p_list.zikatnr
        katpreis.argtnr = arr.argtnr
        katpreis.startperiode = p_list.startperiode
        katpreis.endperiode = p_list.endperiode
        katpreis.betriebsnr = p_list.betriebsnr
        katpreis.perspreis[0] = p_list.perspreis[0]
        katpreis.perspreis[1] = p_list.perspreis[1]
        katpreis.perspreis[2] = p_list.perspreis[2]
        katpreis.perspreis[3] = p_list.perspreis[3]
        katpreis.kindpreis[0] = p_list.kindpreis[0]
        katpreis.kindpreis[1] = p_list.kindpreis[1]

    p_list = query(p_list_list, first=True)

    if case_type == 1:
        katpreis = Katpreis()
        db_session.add(katpreis)

        fill_katpreis()

    elif case_type == 2:

        katpreis = db_session.query(Katpreis).filter(
                (Katpreis._recid == rec_id)).first()

        katpreis = db_session.query(Katpreis).first()
        fill_katpreis()

        katpreis = db_session.query(Katpreis).first()

    return generate_output()