#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def rest_rsvplan2_paymentdetailbl(reservationid:int):

    prepare_cache ([Queasy])

    payment_list_data = []
    queasy = None

    payment_list = None

    payment_list_data, Payment_list = create_model("Payment_list", {"paymentdate":date, "invoicenumber":string, "depositamount":Decimal, "paymentamount":Decimal, "chgdate":date, "chgtime":string, "userinit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment_list_data, queasy
        nonlocal reservationid


        nonlocal payment_list
        nonlocal payment_list_data

        return {"payment-list": payment_list_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 312) & (Queasy.number1 == reservationid)).order_by(Queasy._recid).all():
        payment_list = Payment_list()
        payment_list_data.append(payment_list)

        payment_list.paymentdate = queasy.date2
        payment_list.invoicenumber = queasy.char1
        payment_list.depositamount =  to_decimal(queasy.deci1)
        payment_list.paymentamount =  to_decimal(queasy.deci2)
        payment_list.chgdate = queasy.date1
        payment_list.chgtime = to_string(queasy.number2, "HH:MM:SS")
        payment_list.userinit = queasy.char3

    return generate_output()