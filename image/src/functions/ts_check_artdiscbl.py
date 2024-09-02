from functions.additional_functions import *
import decimal
from models import H_bill_line, Htparam, H_bill

def ts_check_artdiscbl(case_type:int, rechnr:int):
    error_flag = 0
    disc:int = 0
    loopi:int = 0
    h_bill_line = htparam = h_bill = None

    hbline = None

    Hbline = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, disc, loopi, h_bill_line, htparam, h_bill
        nonlocal hbline


        nonlocal hbline
        return {"error_flag": error_flag}


    if case_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()

        if htparam:
            disc = htparam.finteger

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr)).all():

            if h_bill_line.artnr == disc:
                error_flag = 1

                return generate_output()

    elif case_type == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 451)).first()

        if htparam:
            disc = to_int(entry(0, htparam.fchar, ";"))

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr)).all():

            if h_bill_line.artnr == disc:
                error_flag = 1

                return generate_output()

    elif case_type == 3:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 451)).first()

        if htparam:
            disc = to_int(entry(0, htparam.fchar, ";"))

        h_bill = db_session.query(H_bill).filter(
                (H_bill._recid == rechnr)).first()

        if h_bill:

            for h_bill_line in db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == h_bill.rechnr)).all():

                if h_bill_line.artnr == disc:
                    error_flag = 1

                    return generate_output()