#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd 3/8/2025
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, H_artikel, Htparam, H_bill_line

def ts_biltransfer_check_discartbl(rec_id:int, dept:int):

    prepare_cache ([H_bill, H_artikel, Htparam, H_bill_line])

    it_exist = False
    selected_nr = 0
    anzahl = 0
    h_bill = h_artikel = htparam = h_bill_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, selected_nr, anzahl, h_bill, h_artikel, htparam, h_bill_line
        nonlocal rec_id, dept

        return {"it_exist": it_exist, "selected_nr": selected_nr, "anzahl": anzahl}

    def check_discart():

        nonlocal it_exist, selected_nr, anzahl, h_bill, h_artikel, htparam, h_bill_line
        nonlocal rec_id, dept

        disc_art:int = 0
        disc_val:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
        disc_art = htparam.finteger

        if disc_art != 0:

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept) & (H_bill_line.artnr == disc_art)).order_by(H_bill_line._recid).all():
                disc_val =  to_decimal(disc_val) + to_decimal(h_bill_line.betrag)

            if disc_val >= 1 or disc_val <= -1:
                it_exist = True

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    # Rd 3/8/2025
    # if not avail -> return
    if h_bill is None:
        return generate_output()
    
    check_discart()

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == dept) & (H_artikel.artart == 12)).order_by(H_artikel._recid).all():
        selected_nr = h_artikel.artnr
        anzahl = anzahl + 1

    return generate_output()