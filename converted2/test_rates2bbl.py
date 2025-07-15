#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Guest_pr, ratecode, Arrangement, Zimkateg

def test_rates2bbl(gastnr:int, frdate:date, todate:date, ratecode:string):

    prepare_cache ([Queasy, Guest_pr, ratecode, Zimkateg])

    rate_list1_data = []
    x:int = 0
    i:int = 0
    bypax:bool = False
    x1:int = 0
    currrate:string = ""
    rm:string = ""
    currdate:date = None
    queasy = guest_pr = ratecode = arrangement = zimkateg = None

    rate_list1 = rate_list2 = None

    rate_list1_data, Rate_list1 = create_model("Rate_list1", {"origcode":string, "rcode":[Decimal,31], "berates":[Decimal,31]})
    rate_list2_data, Rate_list2 = create_model("Rate_list2")

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_list1_data, x, i, bypax, x1, currrate, rm, currdate, queasy, guest_pr, ratecode, arrangement, zimkateg
        nonlocal gastnr, frdate, todate, ratecode


        nonlocal rate_list1, rate_list2
        nonlocal rate_list1_data, rate_list2_data

        return {"rate-list1": rate_list1_data}

    def create_list():

        nonlocal rate_list1_data, x, i, bypax, x1, currrate, rm, currdate, queasy, guest_pr, ratecode, arrangement, zimkateg
        nonlocal gastnr, frdate, todate, ratecode


        nonlocal rate_list1, rate_list2
        nonlocal rate_list1_data, rate_list2_data

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, ratecode.argtnr)]})

        queasy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, ratecode.zikatnr)]})

        if queasy:
            rm = queasy.char1

        elif not queasy:

            zimkateg = get_cache (Zimkateg, {"typ": [(eq, queasy.number1)]})

            if zimkateg:
                rm = zimkateg.kurzbez
        rate_list1 = Rate_list1()
        rate_list1_data.append(rate_list1)

        rate_list1.origcode = ratecode.code + ":" + rm


        for i in range(1,x + 1) :

            if (frdate + i - 1) >= ratecode.startperiode and (frdate + i - 1) <= ratecode.endperiod and i <= 31:
                rate_list1.rcode[i - 1] = ratecode.zipreis rate_list1.BERates[i - 1] = ratecode.zipreis


    x = (todate - frdate + 1).days
    currdate = frdate - timedelta(days=1)

    queasy = get_cache (Queasy, {"key": [(eq, 160)]})

    if queasy:
        bypax = logical(to_string(entry (2, entry (14, queasy.char1, "$") , "=")))

    if ratecode == "":

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == gastnr)).order_by(Guest_pr._recid).all():

            for ratecode in db_session.query(ratecode).filter(
                     (ratecode.code == guest_pr.code) & (((ratecode.startperiod >= frdate) & (ratecode.startperiod <= todate)) | ((ratecode.endperiod >= frdate) & (ratecode.endperiod <= todate)) | ((ratecode.startperiod < frdate) & (ratecode.endperiod > todate)))).order_by(ratecode._recid).all():
                create_list()
    else:

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == gastnr) & (Guest_pr.code == ratecode)).order_by(Guest_pr._recid).all():

            for ratecode in db_session.query(ratecode).filter(
                     (ratecode.code == guest_pr.code) & (((ratecode.startperiod >= frdate) & (ratecode.startperiod <= todate)) | ((ratecode.endperiod >= frdate) & (ratecode.endperiod <= todate)) | ((ratecode.startperiod < frdate) & (ratecode.endperiod > todate)))).order_by(ratecode._recid).all():
                create_list()

    for rate_list1 in query(rate_list1_data):
        rate_list2 = Rate_list2()
        rate_list2_data.append(rate_list2)

        buffer_copy(rate_list1, rate_list2)

    if bypax == False:

        for rate_list1 in query(rate_list1_data):

            if currrate != rate_list1.origcode:
                x1 = 1
            else:
                x1 = x1 + 1
            currrate = rate_list1.origcode

            if x1 == 2:

                rate_list2 = query(rate_list2_data, filters=(lambda rate_list2: rate_list2.origcode == currrate), first=True)

                if rate_list2:
                    rate_list2_data.remove(rate_list2)

    for rate_list1 in query(rate_list1_data):
        rate_list1_data.remove(rate_list1)
        pass

    for rate_list2 in query(rate_list2_data):
        rate_list1 = Rate_list1()
        rate_list1_data.append(rate_list1)

        buffer_copy(rate_list2, rate_list1)
    for i in range(1,x + 1) :
        currdate = currdate + timedelta(days=1)

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 201) & (Queasy.number1 == 5) & (Queasy.date1 == currdate)).order_by(Queasy._recid.desc()).first()

        if queasy:

            rate_list1 = query(rate_list1_data, filters=(lambda rate_list1: rate_list1.origcode == queasy.char1), first=True)

            if rate_list1:

                if queasy.deci2 != 0:
                    rate_list1.berates[i - 1] = queasy.deci2


                else:
                    rate_list1.berates[i - 1] = queasy.deci3

    return generate_output()