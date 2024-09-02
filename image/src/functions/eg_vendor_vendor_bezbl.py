from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_vendor

def eg_vendor_vendor_bezbl(curr_select:str, vendor_bezeich:str, rec_id:int):
    avail_sub = False
    eg_vendor = None

    queasy1 = None

    Queasy1 = Eg_vendor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_sub, eg_vendor
        nonlocal queasy1


        nonlocal queasy1
        return {"avail_sub": avail_sub}


    eg_vendor = db_session.query(Eg_vendor).filter(
            (Eg_vendor._recid == rec_id)).first()

    if curr_select.lower()  == "chg":

        queasy1 = db_session.query(Queasy1).filter(
                (func.lower(Queasy1.bezeich) == (vendor_bezeich).lower()) &  (Queasy1._recid != eg_vendor._recid)).first()

    elif curr_select.lower()  == "add":

        queasy1 = db_session.query(Queasy1).filter(
                (func.lower(Queasy1.bezeich) == (vendor_bezeich).lower())).first()

    if queasy1:
        avail_sub = True

    return generate_output()