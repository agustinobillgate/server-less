from functions.additional_functions import *
import decimal
from models import H_bill, H_artikel, Htparam, H_bill_line

def ts_biltransfer_check_discartbl(rec_id:int, dept:int):
    it_exist = False
    selected_nr = 0
    anzahl = 0
    h_bill = h_artikel = htparam = h_bill_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, selected_nr, anzahl, h_bill, h_artikel, htparam, h_bill_line


        return {"it_exist": it_exist, "selected_nr": selected_nr, "anzahl": anzahl}

    def check_discart():

        nonlocal it_exist, selected_nr, anzahl, h_bill, h_artikel, htparam, h_bill_line

        disc_art:int = 0
        disc_val:decimal = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()
        disc_art = htparam.finteger

        if disc_art != 0:

            for h_bill_line in db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == dept) &  (H_bill_line.artnr == disc_art)).all():
                disc_val = disc_val + h_bill_line.betrag

            if disc_val >= 1 or disc_val <= -1:
                it_exist = True


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    check_discart()

    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == dept) &  (H_artikel.artart == 12)).all():
        selected_nr = h_artikel.artnr
        anzahl = anzahl + 1

    return generate_output()