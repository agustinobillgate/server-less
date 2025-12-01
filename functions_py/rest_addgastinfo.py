#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, Res_line, Guest, Htparam, Guest_queasy, H_journal, H_artikel, Artikel

def rest_addgastinfo(dept:int, billno:int, inp_resnr:int, inp_line:int, billnr:int, transdate:date):

    prepare_cache ([H_bill, Res_line, Guest, Htparam, Guest_queasy, H_journal, H_artikel, Artikel])

    billdate:date = None
    do_it:bool = False
    pax:int = 0
    h_bill = res_line = guest = htparam = guest_queasy = h_journal = h_artikel = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, do_it, pax, h_bill, res_line, guest, htparam, guest_queasy, h_journal, h_artikel, artikel
        nonlocal dept, billno, inp_resnr, inp_line, billnr, transdate

        return {}


    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"rechnr": [(eq, billno)]})

    if not h_bill:

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_line)]})

    if res_line:

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

    elif inp_resnr > 0:

        guest = get_cache (Guest, {"gastnr": [(eq, inp_resnr)]})

    if not guest:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if transdate != None:
        billdate = transdate
    else:
        billdate = htparam.fdate
    guest_queasy = Guest_queasy()
    db_session.add(guest_queasy)

    guest_queasy.key = "gast-info"
    guest_queasy.gastnr = guest.gastnr
    guest_queasy.number1 = dept
    guest_queasy.number2 = inp_resnr
    guest_queasy.number3 = inp_line
    guest_queasy.date1 = billdate
    guest_queasy.date2 = billdate


    pass
    guest_queasy.char3 = to_string(to_int(guest_queasy.char3) + h_bill.belegung)
    guest_queasy.char1 = to_string(h_bill.rechnr)

    if guest_queasy.date2 < billdate:
        guest_queasy.date2 = billdate

    for h_journal in db_session.query(H_journal).filter(
                 (H_journal.bill_datum == billdate) & (H_journal.departement == dept) & (H_journal.rechnr == billno) & (H_journal.artnr != 0)).order_by(H_journal._recid).all():

        if billnr == 0:
            do_it = True
        else:
            do_it = h_journal.waehrungcode == billnr

        if do_it:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, dept)]})

            if h_artikel and h_artikel.artart == 0:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})

                if artikel:

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        guest_queasy.deci1 =  to_decimal(guest_queasy.deci1) + to_decimal(h_journal.betrag)

                    elif artikel.umsatzart == 6:
                        guest_queasy.deci2 =  to_decimal(guest_queasy.deci2) + to_decimal(h_journal.betrag)


                    else:
                        guest_queasy.deci3 =  to_decimal(guest_queasy.deci3) + to_decimal(h_journal.betrag)


    pass
    pass

    return generate_output()