#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand, L_op

def main_stock_check_adjustmentbl(inv_type:int):
    curr_type = 0
    l_bestand = l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_type, l_bestand, l_op
        nonlocal inv_type

        return {"inv_type": inv_type, "curr_type": curr_type}

    def check_adjustment():

        nonlocal curr_type, l_bestand, l_op
        nonlocal inv_type


        curr_type = inv_type

        if inv_type == 1:

            l_bestand = get_cache (L_bestand, {"artnr": [(le, 2999999)],"lager_nr": [(eq, 0)]})

            if l_bestand:

                l_op = db_session.query(L_op).filter(
                         (L_op.op_art == 3) & (L_op.artnr <= 2999999) & (substring(L_op.lscheinnr, 0, 3) == ("INV").lower())).first()

                if not l_op:
                    curr_type = 0

        elif inv_type == 2:

            l_bestand = get_cache (L_bestand, {"artnr": [(ge, 3000000)],"lager_nr": [(eq, 0)]})

            if l_bestand:

                l_op = db_session.query(L_op).filter(
                         (L_op.op_art == 3) & (L_op.artnr >= 3000000) & (substring(L_op.lscheinnr, 0, 3) == ("INV").lower())).first()

                if not l_op:
                    curr_type = 0

        if inv_type == 3:

            l_op = db_session.query(L_op).filter(
                     (L_op.op_art == 3) & (substring(L_op.lscheinnr, 0, 3) == ("INV").lower())).first()

            if not l_op:
                curr_type = 0


    check_adjustment()

    return generate_output()