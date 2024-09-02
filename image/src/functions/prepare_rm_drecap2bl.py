from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Segment

def prepare_rm_drecap2bl():
    segmtype_exist = False
    long_digit = False
    to_date = None
    tdate = None
    fdate = None
    opening_date = None
    htparam = segment = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal segmtype_exist, long_digit, to_date, tdate, fdate, opening_date, htparam, segment


        return {"segmtype_exist": segmtype_exist, "long_digit": long_digit, "to_date": to_date, "tdate": tdate, "fdate": fdate, "opening_date": opening_date}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    segment = db_session.query(Segment).filter(
            (Segment.betriebsnr > 0)).first()

    if segment:
        segmtype_exist = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    to_date = htparam.fdate - 1
    tdate = htparam.fdate - 1
    fdate = date_mdy(get_month(tdate) , 1, get_year(tdate))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 186)).first()
    opening_date = htparam.fdate

    return generate_output()