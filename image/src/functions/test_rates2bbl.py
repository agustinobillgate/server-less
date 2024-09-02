from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Guest_pr, ratecode, Arrangement, Zimkateg

def test_rates2bbl(gastnr:int, frdate:date, todate:date, ratecode:str):
    rate_list1_list = []
    x:int = 0
    i:int = 0
    bypax:bool = False
    x1:int = 0
    currrate:str = ""
    rm:str = ""
    currdate:date = None
    queasy = guest_pr = ratecode = arrangement = zimkateg = None

    rate_list1 = rate_list2 = None

    rate_list1_list, Rate_list1 = create_model("Rate_list1", {"origcode":str, "rcode":decimal, "berates":decimal})
    rate_list2_list, Rate_list2 = create_model("Rate_list2")


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_list1_list, x, i, bypax, x1, currrate, rm, currdate, queasy, guest_pr, ratecode, arrangement, zimkateg


        nonlocal rate_list1, rate_list2
        nonlocal rate_list1_list, rate_list2_list
        return {"rate-list1": rate_list1_list}

    def create_list():

        nonlocal rate_list1_list, x, i, bypax, x1, currrate, rm, currdate, queasy, guest_pr, ratecode, arrangement, zimkateg


        nonlocal rate_list1, rate_list2
        nonlocal rate_list1_list, rate_list2_list

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == ratecode.argtnr)).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152 and Queasy.number1 == ratecode.zikatnr)).first()

        if queasy:
            rm = queasy.char1

        elif not queasy:

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.typ == queasy.number1)).first()

            if zimkateg:
                rm = zimkateg.kurzbez
        rate_list1 = Rate_list1()
        rate_list1_list.append(rate_list1)

        rate_list1.origcode = ratecode.code + ":" + rm


        for i in range(1,x + 1) :

            if (frdate + i - 1) >= ratecode.startperiode and (frdate + i - 1) <= ratecode.endperiod and i <= 31:
                rate_list1.rcode[i - 1] = ratecode.zipreis rate_list1.BERates[i - 1] = ratecode.zipreis

    x = todate - frdate + 1
    currdate = frdate - 1

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 160)).first()

    if queasy:
        bypax = logical(to_string(entry (2, entry (14, queasy.char1, "$") , " == ")))

    if ratecode == "":

        for guest_pr in db_session.query(Guest_pr).all():

            for ratecode in db_session.query(ratecode).all():
                create_list()
    else:

        for guest_pr in db_session.query(Guest_pr).all():

            for ratecode in db_session.query(ratecode).all():
                create_list()

    for rate_list1 in query(rate_list1_list):
        rate_list2 = Rate_list2()
        rate_list2_list.append(rate_list2)

        buffer_copy(rate_list1, rate_list2)

    if bypax == False:

        for rate_list1 in query(rate_list1_list):

            if currrate != rate_list1.origcode:
                x1 = 1
            else:
                x1 = x1 + 1
            currrate = rate_list1.origcode

            if x1 == 2:

                rate_list2 = query(rate_list2_list, filters=(lambda rate_list2 :rate_list2.origcode == currrate), first=True)

                if rate_list2:
                    rate_list2_list.remove(rate_list2)

    for rate_list1 in query(rate_list1_list):
        rate_list1_list.remove(rate_list1)


    for rate_list2 in query(rate_list2_list):
        rate_list1 = Rate_list1()
        rate_list1_list.append(rate_list1)

        buffer_copy(rate_list2, rate_list1)
    for i in range(1,x + 1) :
        currdate = currdate + 1

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 201 and Queasy.number1 == 5 and Queasy.date1 == currdate)).first()

        if queasy:

            rate_list1 = query(rate_list1_list, filters=(lambda rate_list1 :rate_list1.origcode == queasy.char1), first=True)

            if rate_list1:

                if queasy.deci2 != 0:
                    rate_list1.BERates[i - 1] = queasy.deci2


                else:
                    rate_list1.BERates[i - 1] = queasy.deci3

    return generate_output()