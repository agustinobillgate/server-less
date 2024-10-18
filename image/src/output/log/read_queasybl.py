from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Htparam

def read_queasybl(case_type:int, intkey:int, inpint1:int, inpchar1:str):
    t_queasy_list = []
    i:int = 0
    j:int = 0
    sumuser:int = 0
    sumappr:int = 0
    p_786:str = ""
    queasy = htparam = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, i, j, sumuser, sumappr, p_786, queasy, htparam
        nonlocal case_type, intkey, inpint1, inpchar1


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    if case_type == 1:

        if not queasy or not(queasy.key == intkey and queasy.number1 == inpint1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == intkey) &  (Queasy.number1 == inpint1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 2:

        if not queasy or not(queasy.key == intkey and queasy.char1 == inpchar1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == intkey) &  (Queasy.char1 == inpchar1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 3:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == intkey)).order_by(Queasy.char1).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    elif case_type == 4:

        if not queasy or not(queasy.key == intkey and queasy.char1 == inpchar1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == intkey) &  (Queasy.char1 == inpchar1)).first()

        if not queasy:

            if not queasy or not(queasy.key == intkey and substring(queasy.char1, 0, len(inpchar1)) == inpchar1):
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == intkey) &  (substring(Queasy.char1, 0, len(inpchar1)) == inpchar1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 5:

        if not queasy or not(queasy.key == intkey):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == intkey)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 6:

        if not queasy or not(queasy.key == intkey and queasy.char3 != ""):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == intkey) &  (Queasy.char3 != "")).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 7:

        if not queasy or not(queasy.key == intkey and queasy.number1 == inpint1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == intkey) &  (Queasy.number1 == inpint1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 8:

        if not queasy or not(queasy.key == intkey and queasy.number1 == inpint1 and queasy.char1 == inpchar1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == intkey) &  (Queasy.number1 == inpint1) &  (Queasy.char1 == inpchar1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 9:

        if not queasy or not(queasy.key == 18 and queasy.number1 == intkey and queasy.char3 != ""):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 18) &  (Queasy.number1 == intkey) &  (Queasy.char3 != "")).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 10:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == intkey) &  (Queasy.number3 == inpint1)).order_by(Queasy._recid).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 11:

        if not queasy or not(queasy._recid == intkey):
            queasy = db_session.query(Queasy).filter(
                (Queasy._recid == intkey)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 12:

        if not queasy or not(queasy.number1 == inpint1 and queasy.number2 == 0 and queasy.deci2 == 0 and queasy.key == intkey):
            queasy = db_session.query(Queasy).filter(
                (Queasy.number1 == inpint1) &  (Queasy.number2 == 0) &  (Queasy.deci2 == 0) &  (Queasy.key == intkey)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 13:

        if not queasy or not(queasy.key == intkey and queasy.number1 != inpint1 and queasy.char3 == inpchar1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == intkey) &  (Queasy.number1 != inpint1) &  (Queasy.char3 == inpchar1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 14:

        if not queasy or not(queasy.key == 25 and queasy.number1 == intkey and queasy.number2 == inpint1 and queasy.char3 == inpchar1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 25) &  (Queasy.number1 == intkey) &  (Queasy.number2 == inpint1) &  (Queasy.char3 == inpchar1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 15:

        if not htparam or not(htparam.paramnr == 110):
            htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()

        if inpint1 == 0:

            if not queasy or not(queasy.key == 37 and queasy.betriebsnr == intkey and queasy.date1 == htparam.fdate and queasy.logi1  and queasy.char1.lower()  == ("micros").lower()):
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 37) &  (Queasy.betriebsnr == intkey) &  (Queasy.date1 == htparam.fdate) &  (Queasy.logi1) &  (func.lower(Queasy.char1) == ("micros").lower())).first()
        else:

            if not queasy or not(queasy.key == 37 and queasy.betriebsnr == intkey and queasy.date1 == htparam.fdate and queasy.logi1  and queasy.char1.lower()  == ("micros").lower()  and queasy.number1 == inpint1):
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 37) &  (Queasy.betriebsnr == intkey) &  (Queasy.date1 == htparam.fdate) &  (Queasy.logi1) &  (func.lower(Queasy.char1) == ("micros").lower()) &  (Queasy.number1 == inpint1)).first()

        if queasy:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            pass
    elif case_type == 16:

        if not htparam or not(htparam.paramnr == 110):
            htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 37) &  (Queasy.betriebsnr == intkey) &  (Queasy.date1 == htparam.fdate) &  (Queasy.logi1) &  (func.lower(Queasy.char1) == ("micros").lower()) &  (Queasy.number1 > inpint1)).order_by(Queasy._recid).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            pass

    return generate_output()