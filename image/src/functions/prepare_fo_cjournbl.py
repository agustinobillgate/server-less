from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt

def prepare_fo_cjournbl(from_dept:int):
    fdate = None
    long_digit = False
    depname1 = ""
    depname2 = ""
    htparam = hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, long_digit, depname1, depname2, htparam, hoteldpt


        return {"fdate": fdate, "long_digit": long_digit, "depname1": depname1, "depname2": depname2}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    fdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == from_dept)).first()

    if hoteldpt:
        depname1 = hoteldpt.depart
        depname2 = hoteldpt.depart

    return generate_output()