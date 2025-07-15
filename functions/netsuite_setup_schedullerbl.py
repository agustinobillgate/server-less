#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def netsuite_setup_schedullerbl(case_type:int, month_val:int, week:int, send_date:date, from_date:date, to_date:date):
    if_list_data = []
    queasy = None

    if_list = None

    if_list_data, If_list = create_model("If_list", {"month_val":int, "month_str":string, "week":int, "send_date":date, "fr_date":date, "to_date":date, "sendflag":bool, "resendflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal if_list_data, queasy
        nonlocal case_type, month_val, week, send_date, from_date, to_date


        nonlocal if_list
        nonlocal if_list_data

        return {"if-list": if_list_data}

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 259
        queasy.betriebsnr = get_month(send_date)
        queasy.number1 = week
        queasy.number2 = month_val
        queasy.date1 = send_date
        queasy.date2 = from_date
        queasy.date3 = to_date
        queasy.logi1 = False

    elif case_type == 2:

        queasy = get_cache (Queasy, {"key": [(eq, 259)],"number2": [(eq, month_val)],"number1": [(eq, week)]})

        if queasy:
            queasy.date1 = send_date
            queasy.date2 = from_date
            queasy.date3 = to_date
            queasy.logi1 = False

    elif case_type == 3:

        queasy = get_cache (Queasy, {"key": [(eq, 259)],"number2": [(eq, month_val)],"number1": [(eq, week)]})

        if queasy:
            db_session.delete(queasy)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 259)).order_by(Queasy.number2, Queasy.date1).all():
        if_list = If_list()
        if_list_data.append(if_list)

        if_list.month_val = queasy.number2
        if_list.week = queasy.number1
        if_list.send_date = queasy.date1
        if_list.fr_date = queasy.date2
        if_list.to_date = queasy.date3
        if_list.sendflag = queasy.logi1

        if queasy.number2 == 1:
            if_list.month_str = "January"

        elif queasy.number2 == 2:
            if_list.month_str = "February"

        elif queasy.number2 == 3:
            if_list.month_str = "March"

        elif queasy.number2 == 4:
            if_list.month_str = "April"

        elif queasy.number2 == 5:
            if_list.month_str = "May"

        elif queasy.number2 == 6:
            if_list.month_str = "June"

        elif queasy.number2 == 7:
            if_list.month_str = "July"

        elif queasy.number2 == 8:
            if_list.month_str = "August"

        elif queasy.number2 == 9:
            if_list.month_str = "September"

        elif queasy.number2 == 10:
            if_list.month_str = "October"

        elif queasy.number2 == 11:
            if_list.month_str = "November"

        elif queasy.number2 == 12:
            if_list.month_str = "December"

    return generate_output()