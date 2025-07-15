#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_action

treqdetail_data, Treqdetail = create_model("Treqdetail", {"reqnr":int, "actionnr":int, "action":string, "create_date":date, "create_time":int, "create_str":string, "create_by":string, "flag":bool})

def eg_chgreq_create_actionbl(intmaintask:int, treqdetail_data:[Treqdetail]):

    prepare_cache ([Eg_action])

    taction_data = []
    eg_action = None

    treqdetail = taction = None

    taction_data, Taction = create_model("Taction", {"act_nr":int, "act_nm":string, "selected":bool, "str_sel":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal taction_data, eg_action
        nonlocal intmaintask


        nonlocal treqdetail, taction
        nonlocal taction_data

        return {"taction": taction_data}

    def create_action():

        nonlocal taction_data, eg_action
        nonlocal intmaintask


        nonlocal treqdetail, taction
        nonlocal taction_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_action)

        if intmaintask > 0:

            for qbuff in db_session.query(Qbuff).filter(
                     (Qbuff.maintask == intmaintask)).order_by(Qbuff.bezeich).all():

                taction = query(taction_data, filters=(lambda taction: taction.act_nr == qbuff.actionnr), first=True)

                if taction:
                    taction.act_nm = qbuff.bezeich


                else:

                    treqdetail = query(treqdetail_data, filters=(lambda treqdetail: treqdetail.actionnr == qbuff.actionnr), first=True)

                    if treqdetail:
                        pass
                    else:
                        taction = Taction()
                        taction_data.append(taction)

                        taction.act_nr = qbuff.actionnr
                        taction.act_nm = qbuff.bezeich


        else:

            for qbuff in db_session.query(Qbuff).order_by(Qbuff.bezeich).all():
                taction = Taction()
                taction_data.append(taction)

                taction.act_nr = qbuff.actionnr
                taction.act_nm = qbuff.bezeich


    create_action()

    return generate_output()