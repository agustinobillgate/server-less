from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Zimmer

def ooohist_listbl(from_date:date, to_date:date):
    output_list_list = []
    curr_date:date = None
    queasy = zimmer = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"roomno":str, "roomtype":str, "reason":str, "from_date":date, "to_date":date, "sysdate":date, "userinit":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, curr_date, queasy, zimmer
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}


    output_list_list.clear()
    for curr_date in date_range(from_date,to_date) :

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 900) &  
                ((Queasy.date2 >= curr_date) &  (Queasy.date2 <= curr_date)) |  
                ((Queasy.date2 <= curr_date) &  (Queasy.date3 >= curr_date))
                ).order_by(Queasy.date1).all():

            if not zimmer or not(zimmer.zikatnr == queasy.number1):
                zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == queasy.number1)).first()

            if zimmer:

                if not output_list or not(output_list.roomno == queasy.char1 and output_list.from_date == queasy.date2 and output_list.to_date == queasy.date3):
                    output_list = query(output_list_list, filters=(lambda output_list: output_list.roomno == queasy.char1 and output_list.from_date == queasy.date2 and output_list.to_date == queasy.date3), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.roomno = queasy.char1
                    output_list.roomtype = zimmer.bezeich
                    output_list.reason = entry(0, queasy.char2, "$")
                    output_list.from_date = queasy.date2
                    output_list.to_date = queasy.date3
                    output_list.sysdate = queasy.date1
                    output_list.userinit = queasy.char3

    return generate_output()