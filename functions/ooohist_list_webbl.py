#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Zimmer

def ooohist_list_webbl(from_date:date, to_date:date, rmno:string):

    prepare_cache ([Queasy, Zimmer])

    output_list_data = []
    curr_date:date = None
    num_day:int = 0
    queasy = zimmer = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"roomno":string, "roomtype":string, "reason":string, "from_date":date, "to_date":date, "sysdate":date, "userinit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, curr_date, num_day, queasy, zimmer
        nonlocal from_date, to_date, rmno


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}


    num_day = (to_date - from_date).days
    output_list_data.clear()

    if (rmno != "" and rmno != None) or num_day >= 730:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 900) & (Queasy.date3 >= from_date) & (Queasy.date3 <= to_date)).order_by(Queasy.date1).all():

            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, queasy.number1)]})

            if zimmer:

                output_list = query(output_list_data, filters=(lambda output_list: output_list.roomno == queasy.char1 and output_list.from_date == queasy.date2 and output_list.to_date == queasy.date3), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.roomno = queasy.char1
                    output_list.roomtype = zimmer.bezeich
                    output_list.reason = entry(0, queasy.char2, "$")
                    output_list.from_date = queasy.date2
                    output_list.to_date = queasy.date3
                    output_list.sysdate = queasy.date1
                    output_list.userinit = queasy.char3

        if rmno != "" and rmno != None:

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.roomno != rmno)):
                output_list_data.remove(output_list)
    else:
        for curr_date in date_range(from_date,to_date) :

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 900) & ((Queasy.date2 >= curr_date) & (Queasy.date2 <= curr_date)) | ((Queasy.date2 <= curr_date) & (Queasy.date3 >= curr_date))).order_by(Queasy.date1).all():

                zimmer = get_cache (Zimmer, {"zikatnr": [(eq, queasy.number1)]})

                if zimmer:

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.roomno == queasy.char1 and output_list.from_date == queasy.date2 and output_list.to_date == queasy.date3), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.roomno = queasy.char1
                        output_list.roomtype = zimmer.bezeich
                        output_list.reason = entry(0, queasy.char2, "$")
                        output_list.from_date = queasy.date2
                        output_list.to_date = queasy.date3
                        output_list.sysdate = queasy.date1
                        output_list.userinit = queasy.char3

    return generate_output()