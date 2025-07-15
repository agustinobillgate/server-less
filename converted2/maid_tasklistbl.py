#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Zimmer, Zimkateg, Bediener

def maid_tasklistbl(from_date:date, to_date:date, rpt_flag:int):

    prepare_cache ([Queasy, Htparam, Zimmer, Zimkateg, Bediener])

    maid_tasklist_data = []
    tmp_userinit:string = ""
    queasy = htparam = zimmer = zimkateg = bediener = None

    t_queasy = maid_tasklist = None

    t_queasy_data, T_queasy = create_model_like(Queasy)
    maid_tasklist_data, Maid_tasklist = create_model("Maid_tasklist", {"datum":date, "maidcode":string, "maidname":string, "roomnumber":string, "roomcateg":string, "starttime":string, "endtime":string, "duration":string, "progrestat":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal maid_tasklist_data, tmp_userinit, queasy, htparam, zimmer, zimkateg, bediener
        nonlocal from_date, to_date, rpt_flag


        nonlocal t_queasy, maid_tasklist
        nonlocal t_queasy_data, maid_tasklist_data

        return {"maid-tasklist": maid_tasklist_data}


    if rpt_flag == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        from_date = htparam.fdate
        to_date = from_date

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 196) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date)).order_by(Queasy._recid).all():

        zimmer = get_cache (Zimmer, {"zinr": [(eq, entry(0, queasy.char1, ";"))]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

        if queasy.char1 != "" and num_entries(queasy.char1, ";") >= 2:
            maid_tasklist = Maid_tasklist()
            maid_tasklist_data.append(maid_tasklist)

            maid_tasklist.datum = queasy.date1
            maid_tasklist.maidcode = entry(1, queasy.char1, ";")
            maid_tasklist.roomnumber = entry(0, queasy.char1, ";")
            maid_tasklist.roomcateg = zimkateg.bezeichnung
            maid_tasklist.starttime = to_string(queasy.number1, "HH:MM:SS")
            maid_tasklist.endtime = to_string(queasy.number2, "HH:MM:SS")

            if queasy.number2 != 0:
                maid_tasklist.duration = to_string((queasy.number2 - queasy.number1) , "HH:MM:SS")
            else:
                maid_tasklist.duration = to_string(queasy.number2, "HH:MM:SS")

            if queasy.number2 == 0:
                maid_tasklist.progrestat = "On Going"
            else:
                maid_tasklist.progrestat = "Done"
            tmp_userinit = entry(1, queasy.char1, ";")

            bediener = get_cache (Bediener, {"userinit": [(eq, tmp_userinit)]})

            if bediener:
                maid_tasklist.maidname = bediener.username

    return generate_output()