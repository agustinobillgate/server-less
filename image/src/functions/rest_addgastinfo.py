from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill, Res_line, Guest, Htparam, Guest_queasy, H_journal, H_artikel, Artikel

def rest_addgastinfo(dept:int, billno:int, inp_resnr:int, inp_line:int, billnr:int, transdate:date):
    billdate:date = None
    do_it:bool = False
    pax:int = 0
    h_bill = res_line = guest = htparam = guest_queasy = h_journal = h_artikel = artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, do_it, pax, h_bill, res_line, guest, htparam, guest_queasy, h_journal, h_artikel, artikel


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill.departement == dept) &  (H_bill.rechnr == billno)).first()

    if not h_bill:

        return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == inp_line)).first()

    if res_line:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

    elif inp_resnr > 0:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == inp_resnr)).first()

    if not guest:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()

    if transdate != None:
        billdate = transdate
    else:
        billdate = htparam.fdate
    guest_queasy = Guest_queasy()
    db_session.add(guest_queasy)

    guest_queasy.key = "gast_info"
    guest_queasy.gastnr = guest.gastnr
    guest_queasy.number1 = dept
    guest_queasy.number2 = inp_resnr
    guest_queasy.number3 = inp_line
    guest_queasy.date1 = billdate
    guest_queasy.date2 = billdate

    guest_queasy = db_session.query(Guest_queasy).first()
    guest_queasy.char3 = to_string(to_int(guest_queasy.char3) +\
            h_bill.belegung)
    guest_queasy.char1 = to_string(h_bill.rechnr)

    if guest_queasy.date2 < billdate:
        guest_queasy.date2 = billdate

    for h_journal in db_session.query(H_journal).filter(
                (H_journal.bill_datum == billdate) &  (H_journal.departement == dept) &  (H_journal.rechnr == billno) &  (H_journal.artnr != 0)).all():

        if billnr == 0:
            do_it = True
        else:
            do_it = h_journal.waehrungcode == billnr

        if do_it:

            h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_journal.artnr) &  (H_artikel.departement == dept)).first()

            if h_artikel and h_artikel.artart == 0:

                artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == dept)).first()

                if artikel:

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        guest_queasy.deci1 = guest_queasy.deci1 + h_journal.betrag

                    elif artikel.umsatzart == 6:
                        guest_queasy.deci2 = guest_queasy.deci2 + h_journal.betrag


                    else:
                        guest_queasy.deci3 = guest_queasy.deci3 + h_journal.betrag

    guest_queasy = db_session.query(Guest_queasy).first()

    return generate_output()