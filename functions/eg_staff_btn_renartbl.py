#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_mdetail, Eg_request

def eg_staff_btn_renartbl(staff_nr:int):
    avail_table = False
    eg_mdetail = eg_request = None

    main = req = None

    Main = create_buffer("Main",Eg_mdetail)
    Req = create_buffer("Req",Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_table, eg_mdetail, eg_request
        nonlocal staff_nr
        nonlocal main, req


        nonlocal main, req

        return {"avail_table": avail_table}


    main = db_session.query(Main).filter(
             (Main.key == 2) & (Main.nr == staff_nr)).first()

    req = db_session.query(Req).filter(
             (Req.assign_to == staff_nr)).first()

    if req and main:
        avail_table = True

    return generate_output()