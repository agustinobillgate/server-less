from functions.additional_functions import *
import decimal
from models import Queasy, Tisch

def tbplan_setup_btn_addbl(curr_n:int, location:int, from_table:int):
    err_flag = 0
    queasy = tisch = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, queasy, tisch


        return {"err_flag": err_flag}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 31) &  (Queasy.number1 == location) &  (Queasy.number2 == from_table) &  (Queasy.betriebsnr == 0)).first()

    if queasy:
        err_flag = 1

        return generate_output()

    tisch = db_session.query(Tisch).filter(
            (Tisch.departement == location) &  (Tischnr == from_table)).first()

    if curr_n == 100:
        err_flag = 2

        return generate_output()