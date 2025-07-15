#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, H_artikel, Queasy, H_journal

payload_list_data, Payload_list = create_model("Payload_list", {"v_mode":int, "art_number":int, "dept_number":int, "art_quantity":int})

def ts_general_check_menubl(payload_list_data:[Payload_list]):

    prepare_cache ([Htparam, H_artikel, Queasy, H_journal])

    response_list_data = []
    bill_date:date = None
    max_soldout_qty:int = 0
    current_qty:int = 0
    remain_qty:int = 0
    posted_qty:int = 0
    soldout_flag:bool = False
    art_desc:string = ""
    htparam = h_artikel = queasy = h_journal = None

    payload_list = response_list = None

    response_list_data, Response_list = create_model("Response_list", {"result_msg":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal response_list_data, bill_date, max_soldout_qty, current_qty, remain_qty, posted_qty, soldout_flag, art_desc, htparam, h_artikel, queasy, h_journal


        nonlocal payload_list, response_list
        nonlocal response_list_data

        return {"response-list": response_list_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate
    response_list = Response_list()
    response_list_data.append(response_list)


    payload_list = query(payload_list_data, first=True)

    if not payload_list:
        response_list.result_msg = "No data available."

        return generate_output()

    if payload_list.v_mode == 1:

        for payload_list in query(payload_list_data):
            current_qty = 0
            posted_qty = 0

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, payload_list.art_number)],"departement": [(eq, payload_list.dept_number)]})

            if h_artikel:

                queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_artikel.artnr)],"number3": [(eq, h_artikel.departement)]})

                if queasy:
                    max_soldout_qty = to_int(queasy.deci1)
                    soldout_flag = queasy.logi2


                    art_desc = h_artikel.bezeich

            if max_soldout_qty != 0:

                for h_journal in db_session.query(H_journal).filter(
                         (H_journal.artnr == payload_list.art_number) & (H_journal.departement == payload_list.dept_number) & (H_journal.bill_datum == bill_date)).order_by(H_journal._recid).all():
                    current_qty = current_qty + h_journal.anzahl
                    posted_qty = posted_qty + h_journal.anzahl
                current_qty = current_qty + payload_list.art_quantity
                remain_qty = max_soldout_qty - posted_qty

                if current_qty > max_soldout_qty:
                    response_list.result_msg = "Input qty greater than max soldout qty. Allowed qty = " + to_string(remain_qty) + "." + chr_unicode(10) + to_string(payload_list.art_number) + " - " + art_desc + "." + chr_unicode(10) + "Confirm not possible."

                    return generate_output()

            if soldout_flag:
                response_list.result_msg = "Soldout menu flag already update to be YES with another user. Article:" + chr_unicode(10) + to_string(payload_list.art_number) + " - " + art_desc + chr_unicode(10) + "Please check it and refresh this page."

                return generate_output()
        response_list.result_msg = "Success"

    elif payload_list.v_mode == 2:

        for payload_list in query(payload_list_data):
            current_qty = 0

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, payload_list.art_number)],"departement": [(eq, payload_list.dept_number)]})

            if h_artikel:

                queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_artikel.artnr)],"number3": [(eq, h_artikel.departement)]})

                if queasy:
                    max_soldout_qty = to_int(queasy.deci1)
                    soldout_flag = queasy.logi2

                if max_soldout_qty != 0:

                    for h_journal in db_session.query(H_journal).filter(
                             (H_journal.artnr == payload_list.art_number) & (H_journal.departement == payload_list.dept_number) & (H_journal.bill_datum == bill_date)).order_by(H_journal._recid).all():
                        current_qty = current_qty + h_journal.anzahl

                    if current_qty >= max_soldout_qty:
                        response_list.result_msg = "Transaction has article soldout. Please refresh article list."

                        return generate_output()
        response_list.result_msg = "Success"

    return generate_output()