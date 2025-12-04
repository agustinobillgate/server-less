#using conversion tools version: 1.0.0.119
#-----------------------------------------
# Rd 28/7/2025
# gitlab: 763
# payload:
#-----------------------------------------
"""
Testing:
https://python.staging.e1-vhp.com:10443/dev/vhpFOC/foInvoiceCalcUnitPrice
{
    "request": {
        "autosaldo": true,
        "pricetab": false,
        "doubleCurrency": false,
        "artnr": 1,
        "balance": 0,
        "balanceForeign": 0,
        "billart": 1,
        "vatArtList": [
            0,
            0,
            0,
            0
        ],
        "lvAnzVat": 1,
        "currDepartment": 0,
        "bilRecid": 140195,
        "inputUserkey": "95EE44CBF839764A7690C157AC66C9C902905E01",
        "inputUsername": "it",
        "hotel_schema": "qcserverless3"
    }
}

"""

from functions.additional_functions import *
from decimal import Decimal
from functions.fo_invoice_return_qtybl import fo_invoice_return_qtybl
from functions.fo_invoice_calculate_unitpricebl import fo_invoice_calculate_unitpricebl

def fo_inv_calc_unitprice_listbl(autosaldo:bool, pricetab:bool, double_currency:bool, artnr:int, balance:Decimal, balance_foreign:Decimal, billart:int, vat_art_list:list[int], lvanzvat:int, curr_department:int, bil_recid:int):
    price = to_decimal("0.0")
    exrate = to_decimal("0.0")
    found = False
    msg = 0
    amt:Decimal = to_decimal("0.0")
    ind:int = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price, exrate, found, msg, amt, ind
        nonlocal autosaldo, pricetab, double_currency, artnr, balance, balance_foreign, billart, vat_art_list, lvanzvat, curr_department, bil_recid

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

                if billart == vat_art_list[ind - 1]:
                    found = True

            if not found or curr_department > 0:
                price =  - to_decimal(balance)

                return generate_output()
            
            amt = get_output(fo_invoice_calculate_unitpricebl(billart, bil_recid))
            price =  to_decimal(amt)

    return generate_output()