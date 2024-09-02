from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lieferant

def prepare_ap_debtlistbl():
    gst_flag = False
    l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gst_flag, l_lieferant


        return {"gst_flag": gst_flag}


    l_lieferant = db_session.query(L_lieferant).filter(
            (func.lower(L_lieferant.firma) == "GST")).first()

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()