from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Queasy, Bediener

def hk_rmboy_send_to_mobilebl(rmlist:[Rmlist]):
    success_flag = False
    user_init:str = ""
    ci_date:date = None
    htparam = queasy = bediener = None

    rmlist = None

    rmlist_list, Rmlist = create_model("Rmlist", {"flag":int, "code":str, "zinr":str, "credit":int, "floor":int, "gname":str, "pic":str, "bemerk":str, "rstat":str, "ankunft":date, "abreise":date, "kbezeich":str, "nation":str, "paxnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, user_init, ci_date, htparam, queasy, bediener


        nonlocal rmlist
        nonlocal rmlist_list
        return {"success_flag": success_flag}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = fdate

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 196) &  (Queasy.date1 == ci_date) &  (Queasy.char2 == "") &  (Queasy.number1 == 0) &  (Queasy.number2 == 0)).all():
        db_session.delete(queasy)

    for rmlist in query(rmlist_list):

        bediener = db_session.query(Bediener).filter(
                (Bediener.username == rmlist.pic)).first()
        user_init = bediener.userinit

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 196) &  (entry(0, Queasy.char1, ";") == rmlist.zinr) &  (Queasy.date1 == ci_date)).first()

        if queasy:
            queasy.char1 = " "
            queasy.char1 = rmlist.zinr + ";" + user_init + ";" + to_string(rmlist.credit)
            queasy.char2 = ""
            queasy.number1 = 0
            queasy.number2 = 0

            queasy = db_session.query(Queasy).first()

        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 196
            queasy.char1 = rmlist.zinr + ";" + user_init + ";" + to_string(rmlist.credit)
            queasy.date1 = ci_date


    success_flag = True

    return generate_output()