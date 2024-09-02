from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_action

def eg_chgreq_create_actionbl(intmaintask:int, treqdetail:[Treqdetail]):
    taction_list = []
    eg_action = None

    treqdetail = taction = qbuff = None

    treqdetail_list, Treqdetail = create_model("Treqdetail", {"reqnr":int, "actionnr":int, "action":str, "create_date":date, "create_time":int, "create_str":str, "create_by":str, "flag":bool})
    taction_list, Taction = create_model("Taction", {"act_nr":int, "act_nm":str, "selected":bool, "str_sel":str})

    Qbuff = Eg_action

    db_session = local_storage.db_session

    def generate_output():
        nonlocal taction_list, eg_action
        nonlocal qbuff


        nonlocal treqdetail, taction, qbuff
        nonlocal treqdetail_list, taction_list
        return {"taction": taction_list}

    def create_action():

        nonlocal taction_list, eg_action
        nonlocal qbuff


        nonlocal treqdetail, taction, qbuff
        nonlocal treqdetail_list, taction_list


        Qbuff = Eg_action

        if intmaintask > 0:

            for qbuff in db_session.query(Qbuff).filter(
                    (Qbuff.maintask == intmaintask)).all():

                taction = query(taction_list, filters=(lambda taction :taction.act_nr == qbuff.actionnr), first=True)

                if taction:
                    taction.act_nm = qbuff.bezeich


                else:

                    treqdetail = query(treqdetail_list, filters=(lambda treqdetail :treqdetail.actionnr == qbuff.actionnr), first=True)

                    if treqdetail:
                        pass
                    else:
                        taction = Taction()
                        taction_list.append(taction)

                        taction.act_nr = qbuff.actionnr
                        taction.act_nm = qbuff.bezeich


        else:

            for qbuff in db_session.query(Qbuff).all():
                taction = Taction()
                taction_list.append(taction)

                taction.act_nr = qbuff.actionnr
                taction.act_nm = qbuff.bezeich

    create_action()

    return generate_output()