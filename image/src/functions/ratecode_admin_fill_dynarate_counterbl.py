from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Counters, Ratecode, Queasy, Zimkateg

def ratecode_admin_fill_dynarate_counterbl(r_code:str, dynarate_list_rmtype:str, dynarate_list_rcode:str, dynarate_list_w_day:int):
    curr_counter = 0
    counters = ratecode = queasy = zimkateg = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_counter, counters, ratecode, queasy, zimkateg


        return {"curr_counter": curr_counter}

    def fill_dynarate_counter():

        nonlocal curr_counter, counters, ratecode, queasy, zimkateg

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 50)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 50
            counters.counter_bez = "Counter for Dynamic Ratecode"
            counters.counter = 0


        counters.counter = counters.counter + 1

        counters = db_session.query(Counters).first()
        curr_counter = counters.counter

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (r_code).lower())).first()

        ratecode = db_session.query(Ratecode).first()
        ratecode.char1[4] = "CN" + to_string(curr_counter) + ";" +\
                ratecode.char1[4]

        ratecode = db_session.query(Ratecode).first()

        if dynarate_list_rmtype.lower()  == "*":

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 145) &  (Queasy.char1 == ratecode.code) &  (Queasy.char2 == dynarate_list_rcode) &  (Queasy.number1 == 0) &  (Queasy.deci1 == dynarate_list_w_day)).all():
                queasy.deci2 = curr_counter


        else:

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.kurzbez == dynarate_list_rmtype)).first()

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 145) &  (Queasy.char1 == ratecode.code) &  (Queasy.char2 == dynarate_list_rcode) &  (Queasy.number1 == zimkateg.zikatnr) &  (Queasy.deci1 == dynarate_list_w_day)).all():
                queasy.deci2 = curr_counter

    fill_dynarate_counter()

    return generate_output()