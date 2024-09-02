from functions.additional_functions import *
import decimal
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Bill_line, Artikel, Bill, Htparam

def fo_invoice_calculate_unitpricebl(billart:int, bil_recid:int):
    amt = 0
    serv_vat:bool = False
    serv:decimal = 0
    vat:decimal = 0
    vat2:decimal = 0
    fact:decimal = 1
    bill_line = artikel = bill = htparam = None

    bline = foart = vatbuff = None

    Bline = Bill_line
    Foart = Artikel
    Vatbuff = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amt, serv_vat, serv, vat, vat2, fact, bill_line, artikel, bill, htparam
        nonlocal bline, foart, vatbuff


        nonlocal bline, foart, vatbuff
        return {"amt": amt}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    vatbuff = db_session.query(Vatbuff).filter(
            (vatBuff.artnr == billart) &  (vatBuff.departement == 0)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()
    serv_vat = htparam.flogical

    for bline in db_session.query(Bline).filter(
            (Bline.rechnr == bill.rechnr)).all():

        foart = db_session.query(Foart).filter(
                (Foart.artnr == bline.artnr) &  (Foart.departement == bline.departement)).first()

        if foart and foart.mwst_code == vatBuff.mwst_code:

            if bline.orts_tax != 0:
                amt = amt - bline.orts_tax
            else:
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, foart.artnr, foart.departement, bline.bill_datum))
                vat = vat + vat2

                if vat != 0:
                    amt = amt - bline.betrag * (1 - 1 / (1 + vat))

    return generate_output()