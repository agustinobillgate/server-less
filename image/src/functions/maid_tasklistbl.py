from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Htparam, Zimmer, Zimkateg, Bediener

def maid_tasklistbl(from_date:date, to_date:date, rpt_flag:int):
    maid_tasklist_list = []
    queasy = htparam = zimmer = zimkateg = bediener = None

    t_queasy = maid_tasklist = None

    t_queasy_list, T_queasy = create_model_like(Queasy)
    maid_tasklist_list, Maid_tasklist = create_model("Maid_tasklist", {"datum":date, "maidcode":str, "maidname":str, "roomnumber":str, "roomcateg":str, "starttime":str, "endtime":str, "duration":str, "progrestat":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal maid_tasklist_list, queasy, htparam, zimmer, zimkateg, bediener
        nonlocal from_date, to_date, rpt_flag


        nonlocal t_queasy, maid_tasklist
        nonlocal t_queasy_list, maid_tasklist_list
        return {"maid-tasklist": maid_tasklist_list}


    if rpt_flag == 1:

        if not htparam or not(paramnr == 110):
            htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        from_date = htparam.fdate
        to_date = from_date

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 196) &  (Queasy.date1 >= from_date) &  (Queasy.date1 <= to_date)).order_by(Queasy._recid).all():

        if not zimmer or not(zimmer.zinr == entry(0, queasy.char1, ";")):
            zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == entry(0, queasy.char1, ";"))).first()

        if not zimkateg or not(zimkateg.zikatnr == zimmer.zikatnr):
            zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zimmer.zikatnr)).first()

        if queasy.char1 != "" and num_entries(queasy.char1, ";") >= 2:

            if not bediener or not(bediener.userinit == entry(1, queasy.char1, ";")):
                bediener = db_session.query(Bediener).filter(
                    (Bediener.userinit == entry(1, queasy.char1, ";"))).first()
            maid_tasklist = Maid_tasklist()
            maid_tasklist_list.append(maid_tasklist)

            maid_tasklist.datum = queasy.date1
            maid_tasklist.maidcode = entry(1, queasy.char1, ";")
            maid_tasklist.maidname = bediener.username
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

    return generate_output()