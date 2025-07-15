#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_artikelbl import read_artikelbl
from functions.htplogic import htplogic
from functions.read_bill_line1bl import read_bill_line1bl
from functions.htpdec import htpdec
from models import Bill_line, Artikel

def ns_web_calc_unitpricebl(lvanzvat:int, vat_artlist:[int], billart:int, balance:Decimal, curr_department:int, rechnr:int):
    price = to_decimal("0.0")
    amt:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    serv:Decimal = to_decimal("0.0")
    serv_vat:bool = False
    ind:int = 0
    found:bool = False
    fdecimal:Decimal = to_decimal("0.0")
    bill_line = artikel = None

    t_bill_line = vatbuff = bline = foart = None

    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})
    vatbuff_data, Vatbuff = create_model_like(Artikel)
    bline_data, Bline = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})
    foart_data, Foart = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price, amt, vat, serv, serv_vat, ind, found, fdecimal, bill_line, artikel
        nonlocal lvanzvat, vat_artlist, billart, balance, curr_department, rechnr


        nonlocal t_bill_line, vatbuff, bline, foart
        nonlocal t_bill_line_data, vatbuff_data, bline_data, foart_data

        return {"price": price}

    for ind in range(1,lvanzvat + 1) :

        if billart == vat_artlist[ind - 1]:
            found = True

    if not found or curr_department > 0:
        price =  - to_decimal(balance)

        return generate_output()
    vatbuff_data = get_output(read_artikelbl(billart, 0, None))

    vatbuff = query(vatbuff_data, first=True)
    serv_vat = get_output(htplogic(479))
    bline_data = get_output(read_bill_line1bl(3, 0, rechnr, None, None, None, None, None))

    for bline in query(bline_data):
        foart_data = get_output(read_artikelbl(bline.artnr, bline.departement, None))

        foart = query(foart_data, first=True)

        if foart and foart.mwst_code == vatbuff.mwst_code:

            if bline.orts_tax != 0:
                amt =  to_decimal(amt) - to_decimal(bline.orts_tax)
            else:
                fdecimal = get_output(htpdec(foart.service_code))

                if fdecimal != None:
                    serv =  to_decimal(fdecimal) / to_decimal("100")
                fdecimal = get_output(htpdec(foart.mwst_code))

                if fdecimal != None:
                    vat =  to_decimal(fdecimal) / to_decimal("100")

                    if serv_vat:
                        vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(serv)
                else:
                    vat =  to_decimal("0")

                if vat != 0:
                    amt =  to_decimal(amt) - to_decimal(bline.betrag) * to_decimal((1) - to_decimal("1") / to_decimal((1) + to_decimal(vat)))
    price =  to_decimal(amt)

    return generate_output()