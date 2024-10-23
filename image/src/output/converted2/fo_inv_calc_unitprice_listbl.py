from functions.additional_functions import *
import decimal
from functions.fo_invoice_return_qtybl import fo_invoice_return_qtybl
from functions.fo_invoice_calculate_unitpricebl import fo_invoice_calculate_unitpricebl

def fo_inv_calc_unitprice_listbl(autosaldo:bool, pricetab:bool, double_currency:bool, artnr:int, balance:decimal, balance_foreign:decimal, billart:int, vat_artlist:int, lvanzvat:int, curr_department:int, bil_recid:int):
    price = to_decimal("0.0")
    exrate = to_decimal("0.0")
    found = False
    msg = 0
    amt:decimal = to_decimal("0.0")
    ind:int = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price, exrate, found, msg, amt, ind
        nonlocal autosaldo, pricetab, double_currency, artnr, balance, balance_foreign, billart, vat_artlist, lvanzvat, curr_department, bil_recid


        return {"price": price, "exrate": exrate, "found": found, "msg": msg}


    if autosaldo:

        if pricetab or double_currency:

            if double_currency:

                if pricetab:
                    price =  - to_decimal(balance_foreign)
                else:
                    price =  - to_decimal(balance)
            else:
                exrate, price, msg = get_output(fo_invoice_return_qtybl(artnr, balance))
        else:
            for ind in range(1,lvanzvat + 1) :

                if billart == vat_artlist[ind - 1]:
                    found = True

            if not found or curr_department > 0:
                price =  - to_decimal(balance)

                return generate_output()
            amt = get_output(fo_invoice_calculate_unitpricebl(billart, bil_recid))
            price =  to_decimal(amt)

    return generate_output()