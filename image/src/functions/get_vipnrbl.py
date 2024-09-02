from functions.additional_functions import *
import decimal
from models import Htparam

def get_vipnrbl():
    vipnr1 = 0
    vipnr2 = 0
    vipnr3 = 0
    vipnr4 = 0
    vipnr5 = 0
    vipnr6 = 0
    vipnr7 = 0
    vipnr8 = 0
    vipnr9 = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, htparam


        return {"vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9}

    def get_vipnr():

        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, htparam

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 700)).first()

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 701)).first()

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 702)).first()

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 703)).first()

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 704)).first()

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 705)).first()

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 706)).first()

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 707)).first()

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 708)).first()

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger

    get_vipnr()

    return generate_output()