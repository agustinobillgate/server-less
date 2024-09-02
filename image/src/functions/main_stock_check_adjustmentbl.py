from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_bestand, L_op

def main_stock_check_adjustmentbl(inv_type:int):
    curr_type = 0
    l_bestand = l_op = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_type, l_bestand, l_op


        return {"curr_type": curr_type}

    def check_adjustment():

        nonlocal curr_type, l_bestand, l_op


        curr_type = inv_type

        if inv_type == 1:

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr <= 2999999) &  (L_bestand.lager_nr == 0)).first()

            if l_bestand:

                l_op = db_session.query(L_op).filter(
                        (L_op.op_art == 3) &  (L_op.artnr <= 2999999) &  (substring(L_op.lscheinnr, 0, 3) == "INV")).first()

                if not l_op:
                    curr_type = 0

        elif inv_type == 2:

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr >= 3000000) &  (L_bestand.lager_nr == 0)).first()

            if l_bestand:

                l_op = db_session.query(L_op).filter(
                        (L_op.op_art == 3) &  (L_op.artnr >= 3000000) &  (substring(L_op.lscheinnr, 0, 3) == "INV")).first()

                if not l_op:
                    curr_type = 0

        if inv_type == 3:

            l_op = db_session.query(L_op).filter(
                    (L_op.op_art == 3) &  (substring(L_op.lscheinnr, 0, 3) == "INV")).first()

            if not l_op:
                curr_type = 0

    check_adjustment()

    return generate_output()