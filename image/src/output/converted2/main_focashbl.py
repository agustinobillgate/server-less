#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Billjournal, Artikel, Res_history

def main_focashbl(all_user:bool, user_init:string, ci_date:date, shift:int, bediener_nr:int):

    prepare_cache ([Billjournal, Artikel, Res_history])

    billjournal = artikel = res_history = None

    journal = None

    Journal = create_buffer("Journal",Billjournal)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billjournal, artikel, res_history
        nonlocal all_user, user_init, ci_date, shift, bediener_nr
        nonlocal journal


        nonlocal journal

        return {}


    for artikel in db_session.query(Artikel).filter(
             ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.departement == 0)).order_by(Artikel._recid).all():

        if not all_user:

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.userinit == (user_init).lower()) & (Billjournal.artnr == artikel.artnr) & (Billjournal.anzahl != 0) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == ci_date) & (Billjournal.betriebsnr == 0)).order_by(Billjournal._recid).all():

                journal = get_cache (Billjournal, {"_recid": [(eq, billjournal._recid)]})

                if journal:
                    pass
                    journal.betriebsnr = shift
                    pass
                    pass

        else:

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.artnr == artikel.artnr) & (Billjournal.anzahl != 0) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == ci_date) & (Billjournal.betriebsnr == 0)).order_by(Billjournal._recid).all():

                journal = get_cache (Billjournal, {"_recid": [(eq, billjournal._recid)]})

                if journal:
                    pass
                    journal.betriebsnr = shift
                    pass
                    pass


    if all_user:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener_nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Close shift(ALL)"
        res_history.action = "FO Cashier"


        pass
        pass

    return generate_output()