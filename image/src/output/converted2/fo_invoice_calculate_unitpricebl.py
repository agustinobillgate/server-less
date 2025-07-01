#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Bill_line, Artikel, Bill, Htparam

def fo_invoice_calculate_unitpricebl(billart:int, bil_recid:int):

    prepare_cache ([Bill_line, Artikel, Bill, Htparam])

    amt = to_decimal("0.0")
    serv_vat:bool = False
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = 1
    bill_line = artikel = bill = htparam = None

    bline = foart = vatbuff = None

    Bline = create_buffer("Bline",Bill_line)
    Foart = create_buffer("Foart",Artikel)
    Vatbuff = create_buffer("Vatbuff",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amt, serv_vat, serv, vat, vat2, fact, bill_line, artikel, bill, htparam
        nonlocal billart, bil_recid
        nonlocal bline, foart, vatbuff


        nonlocal bline, foart, vatbuff

        return {"amt": amt}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    vatbuff = get_cache (Artikel, {"artnr": [(eq, billart)],"departement": [(eq, 0)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_vat = htparam.flogical

    for bline in db_session.query(Bline).filter(
             (Bline.rechnr == bill.rechnr)).order_by(Bline._recid).all():

        foart = get_cache (Artikel, {"artnr": [(eq, bline.artnr)],"departement": [(eq, bline.departement)]})

        if foart and foart.mwst_code == vatbuff.mwst_code:

            if bline.orts_tax != 0:
                amt =  to_decimal(amt) - to_decimal(bline.orts_tax)
            else:
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, foart.artnr, foart.departement, bline.bill_datum))
                vat =  to_decimal(vat) + to_decimal(vat2)

                if vat != 0:
                    amt =  to_decimal(amt) - to_decimal(bline.betrag) * to_decimal((1) - to_decimal("1") / to_decimal((1) + to_decimal(vat)))

    return generate_output()