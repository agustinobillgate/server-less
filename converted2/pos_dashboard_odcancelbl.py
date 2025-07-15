#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Queasy, Bediener

def pos_dashboard_odcancelbl(from_date:date, to_date:date, from_dept:int, to_dept:int):

    prepare_cache ([Hoteldpt, Queasy, Bediener])

    cancellation_list_data = []
    hoteldpt = queasy = bediener = None

    cancellation_list = None

    cancellation_list_data, Cancellation_list = create_model("Cancellation_list", {"bill_date":date, "table_no":int, "bill_no":int, "order_no":int, "article_no":int, "article_name":string, "cancel_reason":string, "qty":int, "amount":Decimal, "dept_name":string, "cancel_time":string, "cancel_id":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cancellation_list_data, hoteldpt, queasy, bediener
        nonlocal from_date, to_date, from_dept, to_dept


        nonlocal cancellation_list
        nonlocal cancellation_list_data

        return {"cancellation-list": cancellation_list_data}

    def create_cancellation():

        nonlocal cancellation_list_data, hoteldpt, queasy, bediener
        nonlocal from_date, to_date, from_dept, to_dept


        nonlocal cancellation_list
        nonlocal cancellation_list_data

        curr_date:date = None
        canceled_name:string = ""
        cancellation_list_data.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 225) & (Queasy.char1 == ("orderbill-line").lower()) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date) & (to_int(entry(0, Queasy.char2, "|")) == hoteldpt.num) & (num_entries(Queasy.char3, "|") > 8)).order_by(Queasy.date1, Queasy.number2, entry(9, Queasy.char3, "|")).all():

                bediener = get_cache (Bediener, {"userinit": [(eq, entry(10, queasy.char3, "|"))]})

                if bediener:
                    canceled_name = bediener.username
                cancellation_list = Cancellation_list()
                cancellation_list_data.append(cancellation_list)

                cancellation_list.bill_date = queasy.date1
                cancellation_list.table_no = queasy.number2
                cancellation_list.order_no = queasy.number1
                cancellation_list.article_no = to_int(entry(1, queasy.char3, "|"))
                cancellation_list.article_name = entry(2, queasy.char3, "|")
                cancellation_list.cancel_reason = entry(8, queasy.char3, "|")
                cancellation_list.qty = to_int(entry(3, queasy.char3, "|"))
                cancellation_list.dept_name = hoteldpt.depart
                cancellation_list.cancel_time = entry(9, queasy.char3, "|")
                cancellation_list.cancel_id = canceled_name

    create_cancellation()

    return generate_output()