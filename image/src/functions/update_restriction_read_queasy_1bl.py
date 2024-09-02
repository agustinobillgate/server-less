from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Htparam, Zimkateg, Guest

def update_restriction_read_queasy_1bl(rcode:str, rmtype:str, ota:str):
    t_list_list = []
    roomnr:int = 0
    i:int = 0
    end_month:int = 0
    cat_flag:bool = False
    datum:date = None
    ci_date:date = None
    to_date:date = None
    prev_day:int = 0
    curr_anz:int = 0
    otanr:int = 0
    mm:int = 0
    yy:int = 0
    queasy = htparam = zimkateg = guest = None

    t_list = qbuff = None

    t_list_list, T_list = create_model("T_list", {"datum":date, "stat":str})

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, roomnr, i, end_month, cat_flag, datum, ci_date, to_date, prev_day, curr_anz, otanr, mm, yy, queasy, htparam, zimkateg, guest
        nonlocal qbuff


        nonlocal t_list, qbuff
        nonlocal t_list_list
        return {"t-list": t_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 152)).first()

    if queasy:
        cat_flag = True

    if cat_flag:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152) &  (func.lower(Queasy.char1) == (rmtype).lower())).first()

        if queasy:
            roomnr = queasy.number1
    else:

        zimkateg = db_session.query(Zimkateg).filter(
                (func.lower(Zimkateg.kurzbez) == (rmtype).lower())).first()

        if zimkateg:
            roomnr = zimkateg.zikatnr

    if ota.lower()  != "" and ota.lower()  != "*":

        guest = db_session.query(Guest).filter(
                (Guest.karteityp == 2) &  (Guest.steuernr != "") &  (trim(entry(0, Guest.steuernr, "|Guest.")) == (ota).lower())).first()

        if guest:
            otanr = guest.gastnr

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 174) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.number1 == roomnr) &  (Queasy.number3 == otanr) &  (Queasy.date1 == None)).first()
    while None != queasy:
        yy = queasy.number2
        datum = date_mdy(01, 01, yy) - 1
        for i in range(1,num_entries(queasy.char2, ";") - 1 + 1) :
            datum = datum + 1

            if to_int(entry(i - 1, queasy.char2, ";")) != 0:
                qbuff = Qbuff()
                db_session.add(qbuff)

                qbuff.key = 174
                qbuff.date1 = datum
                qbuff.number1 = roomnr
                qbuff.number3 = otanr
                qbuff.char1 = rcode

                if to_int(entry(i - 1, queasy.char2, ";")) == 1:
                    qbuff.char2 = "1;0;0"

                elif to_int(entry(i - 1, queasy.char2, ";")) == 2:
                    qbuff.char2 = "0;1;0"

                elif to_int(entry(i - 1, queasy.char2, ";")) == 3:
                    qbuff.char2 = "0;0;1"

                elif to_int(entry(i - 1, queasy.char2, ";")) == 4:
                    qbuff.char2 = "0;1;1"

        queasy = db_session.query(Queasy).first()
        db_session.delete(queasy)


        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 174) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.number1 == roomnr) &  (Queasy.number3 == otanr) &  (Queasy.date1 == None)).first()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 174) &  (Queasy.date1 < ci_date - 30)).all():
        db_session.delete(queasy)

    to_date = ci_date + 365

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 174) &  (Queasy.date1 >= ci_date) &  (Queasy.date1 <= to_date) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.number1 == roomnr) &  (Queasy.number3 == otanr)).all():
        t_list = T_list()
        t_list_list.append(t_list)

        t_list.datum = queasy.date1
        t_list.stat = queasy.char2

    return generate_output()