from functions.additional_functions import *
import decimal
from functions.read_artikelbl import read_artikelbl
from functions.htplogic import htplogic
from functions.read_bill_line1bl import read_bill_line1bl
from functions.htpdec import htpdec
from models import Bill_line, Artikel

def ns_web_calc_unitpricebl(lvanzvat:int, vat_artlist:int, billart:int, balance:decimal, curr_department:int, rechnr:int):
    price = 0
    amt:decimal = 0
    vat:decimal = 0
    serv:decimal = 0
    serv_vat:bool = False
    ind:int = 0
    found:bool = False
    fdecimal:decimal = 0
    bill_line = artikel = None

    t_bill_line = vatbuff = bline = foart = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    vatbuff_list, Vatbuff = create_model_like(Artikel)
    bline_list, Bline = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    foart_list, Foart = create_model_like(Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price, amt, vat, serv, serv_vat, ind, found, fdecimal, bill_line, artikel


        nonlocal t_bill_line, vatbuff, bline, foart
        nonlocal t_bill_line_list, vatbuff_list, bline_list, foart_list
        return {"price": price}

    for ind in range(1,lvanzvat + 1) :

        if billart == vat_artlist[ind - 1]:
            found = True

    if not found or curr_department > 0:
        price = - balance

        return generate_output()
    vatBuff_list = get_output(read_artikelbl(billart, 0, None))

    vatbuff = query(vatbuff_list, first=True)
    serv_vat = get_output(htplogic(479))
    bline_list = get_output(read_bill_line1bl(3, 0, rechnr, None, None, None, None, None))

    for bline in query(bline_list):
        foart_list = get_output(read_artikelbl(bline.artnr, bline.departement, None))

        foart = query(foart_list, first=True)

        if foart and foart.mwst_code == vatBuff.mwst_code:

            if bline.orts_tax != 0:
                amt = amt - bline.orts_tax
            else:
                fdecimal = get_output(htpdec(foart.service_code))

                if fdecimal != None:
                    serv = fdecimal / 100
                fdecimal = get_output(htpdec(foart.mwst_code))

                if fdecimal != None:
                    vat = fdecimal / 100

                    if serv_vat:
                        vat = vat + vat * serv
                else:
                    vat = 0

                if vat != 0:
                    amt = amt - bline.betrag * (1 - 1 / (1 + vat))
    price = amt

    return generate_output()