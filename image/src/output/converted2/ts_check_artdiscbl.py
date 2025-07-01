#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line, Htparam, H_bill

def ts_check_artdiscbl(case_type:int, rechnr:int):

    prepare_cache ([H_bill_line, Htparam, H_bill])

    error_flag = 0
    disc:int = 0
    loopi:int = 0
    h_bill_line = htparam = h_bill = None

    hbline = None

    Hbline = create_buffer("Hbline",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, disc, loopi, h_bill_line, htparam, h_bill
        nonlocal case_type, rechnr
        nonlocal hbline


        nonlocal hbline

        return {"error_flag": error_flag}


    if case_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

        if htparam:
            disc = htparam.finteger

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr)).order_by(H_bill_line._recid).all():

            if h_bill_line.artnr == disc:
                error_flag = 1

                return generate_output()

    elif case_type == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 451)]})

        if htparam:
            disc = to_int(entry(0, htparam.fchar, ";"))

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr)).order_by(H_bill_line._recid).all():

            if h_bill_line.artnr == disc:
                error_flag = 1

                return generate_output()

    elif case_type == 3:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 451)]})

        if htparam:
            disc = to_int(entry(0, htparam.fchar, ";"))

        h_bill = get_cache (H_bill, {"_recid": [(eq, rechnr)]})

        if h_bill:

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.rechnr == h_bill.rechnr)).order_by(H_bill_line._recid).all():

                if h_bill_line.artnr == disc:
                    error_flag = 1

                    return generate_output()

    return generate_output()