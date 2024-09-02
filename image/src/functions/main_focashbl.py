from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Billjournal, Artikel, Res_history

def main_focashbl(all_user:bool, user_init:str, ci_date:date, shift:int, bediener_nr:int):
    billjournal = artikel = res_history = None

    journal = None

    Journal = Billjournal

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billjournal, artikel, res_history
        nonlocal journal


        nonlocal journal
        return {}


    for artikel in db_session.query(Artikel).filter(
            ((Artikel.artart == 2) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.departement == 0)).all():

        if not all_user:

            for billjournal in db_session.query(Billjournal).filter(
                    (func.lower(Billjournal.userinit) == (user_init).lower()) &  (Billjournal.artnr == artikel.artnr) &  (Billjournal.anzahl != 0) &  (Billjournal.departement == artikel.departement) &  (Billjournal.bill_datum == ci_date) &  (Billjournal.betriebsnr == 0)).all():

                journal = db_session.query(Journal).filter(
                            (Journal._recid == billJournal._recid)).first()
                journal.betriebsnr = shift

                journal = db_session.query(Journal).first()

        else:

            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.artnr == artikel.artnr) &  (Billjournal.anzahl != 0) &  (Billjournal.departement == artikel.departement) &  (Billjournal.bill_datum == ci_date) &  (Billjournal.betriebsnr == 0)).all():

                journal = db_session.query(Journal).filter(
                            (Journal._recid == billJournal._recid)).first()
                journal.betriebsnr = shift

                journal = db_session.query(Journal).first()


    if all_user:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener_nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Close shift(ALL)"
        res_history.action = "FO Cashier"

        res_history = db_session.query(Res_history).first()


    return generate_output()