from functions.additional_functions import *
import decimal
from models import Artikel, Bill, Guest

def fo_invoice_gcf_ccardnumbl(t_rechnr:int, t_artnr:int, curr_department:int):
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
        ch:str = ""
        pos2:int = 0
        gast = None
        Gast =  create_buffer("Gast",Guest)

        gast = db_session.query(Gast).filter(
                 (Gast.gastnr == bill.gastnr)).first()
        for i in range(1,num_entries(gast.ausweis_nr2, "|")  + 1) :
            ch = entry(i - 1, gast.ausweis_nr2, "|")

            if re.match(r".*" + artikel.bezeich + r".*",ch, re.IGNORECASE):
                ch = entry(1, ch, "\\")

                if num_entries(ch, "\\") == 2:
                    mm = to_int(substring(entry(1, ch, "\\") , 0, 2))
                    yy = to_int(substring(entry(1, ch, "\\") , 2, 4))

                    if yy > get_year(get_current_date()) or (yy == get_year(get_current_date()) and mm >= get_month(get_current_date())):
                        voucher_nr = trim(entry(0, ch, "\\"))

                elif num_entries(ch, "\\") == 1:
                    voucher_nr = trim(ch)

                return

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == t_artnr) & (Artikel.departement == curr_department)).first()

    bill = db_session.query(Bill).filter(
             (Bill.rechnr == t_rechnr)).first()
    gcf_ccardnum()

    return generate_output()