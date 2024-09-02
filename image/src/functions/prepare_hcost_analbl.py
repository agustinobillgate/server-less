from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_hcost_analbl():
    long_digit = False
    price_decimal = 0
    to_date = None
    from_date = None
    bill_date = None
    f_eknr = 0
    b_eknr = 0
    fl_eknr = 0
    bl_eknr = 0
    bev_food = ""
    food_bev = ""
    price_type = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, price_decimal, to_date, from_date, bill_date, f_eknr, b_eknr, fl_eknr, bl_eknr, bev_food, food_bev, price_type, htparam


        return {"long_digit": long_digit, "price_decimal": price_decimal, "to_date": to_date, "from_date": from_date, "bill_date": bill_date, "f_eknr": f_eknr, "b_eknr": b_eknr, "fl_eknr": fl_eknr, "bl_eknr": bl_eknr, "bev_food": bev_food, "food_bev": food_bev, "price_type": price_type}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    to_date = fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 862)).first()
    f_eknr = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 892)).first()
    b_eknr = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    fl_eknr = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    bl_eknr = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 272)).first()
    bev_food = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 275)).first()
    food_bev = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1024)).first()
    price_type = htparam.finteger

    return generate_output()