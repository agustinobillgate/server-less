#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line

def ts_restinv_btn_ccardbl(rechnr:int, departement:int):
    flag = False
    h_bill_line = None

    sp_bline = None

    Sp_bline = create_buffer("Sp_bline",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_bill_line
        nonlocal rechnr, departement
        nonlocal sp_bline


        nonlocal sp_bline

        return {"flag": flag}


    sp_bline = db_session.query(Sp_bline).filter(
             (Sp_bline.rechnr == rechnr) & (Sp_bline.departement == departement) & (Sp_bline.waehrungsnr > 0)).first()

    if sp_bline:
        flag = True

        return generate_output()

    return generate_output()