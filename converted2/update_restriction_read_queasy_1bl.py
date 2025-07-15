#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Zimkateg

def update_restriction_read_queasy_1bl(rcode:string, rmtype:string, ota:string):

    prepare_cache ([Queasy, Htparam, Zimkateg])

    t_list_data = []
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
    queasy = htparam = zimkateg = None

    t_list = qbuff = None

    t_list_data, T_list = create_model("T_list", {"datum":date, "stat":string})

    Qbuff = create_buffer("Qbuff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, roomnr, i, end_month, cat_flag, datum, ci_date, to_date, prev_day, curr_anz, otanr, mm, yy, queasy, htparam, zimkateg
        nonlocal rcode, rmtype, ota
        nonlocal qbuff


        nonlocal t_list, qbuff
        nonlocal t_list_data

        return {"t-list": t_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    if cat_flag:

        queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, rmtype)]})

        if queasy:
            roomnr = queasy.number1
    else:

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

        if zimkateg:
            roomnr = zimkateg.zikatnr

    queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode)],"number1": [(eq, roomnr)],"number3": [(eq, otanr)],"date1": [(eq, None)]})
    while None != queasy:
        yy = queasy.number2
        datum = date_mdy(1, 1, yy) - timedelta(days=1)
        for i in range(1,num_entries(queasy.char2, ";") - 1 + 1) :
            datum = datum + timedelta(days=1)

            if to_int(entry(i - 1, queasy.char2, ";")) != 0:
                qbuff = Queasy()
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
        pass
        db_session.delete(queasy)
        pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 174) & (Queasy.char1 == (rcode).lower()) & (Queasy.number1 == roomnr) & (Queasy.number3 == otanr) & (Queasy.date1 == None) & (Queasy._recid > curr_recid)).first()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 174) & (Queasy.date1 < ci_date - timedelta(days=30))).order_by(Queasy._recid).all():
        db_session.delete(queasy)
        pass
    to_date = ci_date + timedelta(days=365)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 174) & (Queasy.date1 >= ci_date) & (Queasy.date1 <= to_date) & (Queasy.char1 == (rcode).lower()) & (Queasy.number1 == roomnr) & (Queasy.number3 == otanr)).order_by(Queasy._recid).all():
        t_list = T_list()
        t_list_data.append(t_list)

        t_list.datum = queasy.date1
        t_list.stat = queasy.char2

    return generate_output()