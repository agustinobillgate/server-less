from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Hoteldpt, Queasy, Bediener

def pos_dashboard_odcancelbl(from_date:date, to_date:date, from_dept:int, to_dept:int):
    cancellation_list_list = []
    hoteldpt = queasy = bediener = None

    cancellation_list = None

    cancellation_list_list, Cancellation_list = create_model("Cancellation_list", {"bill_date":date, "table_no":int, "bill_no":int, "order_no":int, "article_no":int, "article_name":str, "cancel_reason":str, "qty":int, "amount":decimal, "dept_name":str, "cancel_time":str, "cancel_id":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cancellation_list_list, hoteldpt, queasy, bediener


        nonlocal cancellation_list
        nonlocal cancellation_list_list
        return {"cancellation-list": cancellation_list_list}

    def create_cancellation():

        nonlocal cancellation_list_list, hoteldpt, queasy, bediener


        nonlocal cancellation_list
        nonlocal cancellation_list_list

        curr_date:date = None
        canceled_name:str = ""
        cancellation_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill_line") &  (Queasy.date1 >= from_date) &  (Queasy.date1 <= to_date) &  (to_int(entry(0, Queasy.char2, "|Queasy.Queasy.")) == hoteldpt.num) &  (num_entries(Queasy.char3, "|Queasy.") > 8)).all():

                bediener = db_session.query(Bediener).filter(
                        (Bediener.userinit == entry(10, queasy.char3, "|"))).first()

                if bediener:
                    canceled_name = bediener.username
                cancellation_list = Cancellation_list()
                cancellation_list_list.append(cancellation_list)

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