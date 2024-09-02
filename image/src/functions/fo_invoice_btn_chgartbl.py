from functions.additional_functions import *
import decimal
from models import Hoteldpt

def fo_invoice_btn_chgartbl(new_dept:int):
    hotel_depart = ""
    hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hotel_depart, hoteldpt


        return {"hotel_depart": hotel_depart}


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == new_dept)).first()
    hotel_depart = hoteldpt.depart

    return generate_output()