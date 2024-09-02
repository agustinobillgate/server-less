from functions.additional_functions import *
import decimal
from models import Eg_vendor

def eg_chgreq_vendor_nrbl(v_vendor_nr:int):
    avail_ven = False
    ven_bezeich = ""
    eg_vendor = None

    ven = None

    Ven = Eg_vendor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_ven, ven_bezeich, eg_vendor
        nonlocal ven


        nonlocal ven
        return {"avail_ven": avail_ven, "ven_bezeich": ven_bezeich}


    ven = db_session.query(Ven).filter(
            (Ven.vendor_nr == v_vendor_nr)).first()

    if ven:
        ven_bezeich = ven.bezeich
        avail_ven = True

    return generate_output()