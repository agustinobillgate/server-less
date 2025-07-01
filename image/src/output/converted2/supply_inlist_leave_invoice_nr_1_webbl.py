#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_ophdr, L_op, Queasy

def supply_inlist_leave_invoice_nr_1_webbl(h_recid:int, artnr:int, invoice_nr:string, serial_number:string, invoice_date:date):

    prepare_cache ([L_ophdr, L_op, Queasy])

    l_ophdr = l_op = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr, l_op, queasy
        nonlocal h_recid, artnr, invoice_nr, serial_number, invoice_date

        return {}


    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, h_recid)]})

    if l_ophdr:
        l_ophdr.fibukonto = trim(invoice_nr)
        pass

        for l_op in db_session.query(L_op).filter(
                 (L_op.lscheinnr == l_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 1)).order_by(L_op._recid).all():

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 335
                queasy.char1 = l_op.lscheinnr
                queasy.number1 = l_op.artnr
                queasy.date1 = l_op.datum
                queasy.char2 = serial_number

                if queasy.number1 == artnr:
                    queasy.date2 = invoice_date
            else:
                pass
                queasy.char2 = serial_number

                if queasy.number1 == artnr:
                    queasy.date2 = invoice_date
                pass
                pass

    return generate_output()