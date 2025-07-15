#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Bill, Guest

def fo_invoice_gcf_ccardnumbl(t_rechnr:int, t_artnr:int, curr_department:int):

    prepare_cache ([Bill, Guest])

    voucher_nr = ""
    artikel = bill = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal voucher_nr, artikel, bill, guest
        nonlocal t_rechnr, t_artnr, curr_department

        return {"voucher_nr": voucher_nr}

    def gcf_ccardnum():

        nonlocal voucher_nr, artikel, bill, guest
        nonlocal t_rechnr, t_artnr, curr_department

        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        mm:int = 0
        yy:int = 0
        ch:string = ""
        pos2:int = 0
        gast = None
        Gast =  create_buffer("Gast",Guest)

        gast = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
        for i in range(1,num_entries(gast.ausweis_nr2, "|")  + 1) :
            ch = entry(i - 1, gast.ausweis_nr2, "|")

            if matches(ch,r"*" + artikel.bezeich + r"*"):
                ch = entry(1, ch, "\\")

                if num_entries(ch, "\\") == 2:
                    mm = to_int(substring(entry(1, ch, "\\") , 0, 2))
                    yy = to_int(substring(entry(1, ch, "\\") , 2, 4))

                    if yy > get_year(get_current_date()) or (yy == get_year(get_current_date()) and mm >= get_month(get_current_date())):
                        voucher_nr = trim(entry(0, ch, "\\"))

                elif num_entries(ch, "\\") == 1:
                    voucher_nr = trim(ch)

                return

    artikel = get_cache (Artikel, {"artnr": [(eq, t_artnr)],"departement": [(eq, curr_department)]})

    bill = get_cache (Bill, {"rechnr": [(eq, t_rechnr)]})
    gcf_ccardnum()

    return generate_output()