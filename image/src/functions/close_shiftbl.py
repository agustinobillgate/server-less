from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Billjournal, Artikel

def close_shiftbl(user_init:str, from_date:date, shift:int):
    billjournal = artikel = None

    journal = None

    Journal = Billjournal

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billjournal, artikel
        nonlocal journal


        nonlocal journal
        return {}


    for artikel in db_session.query(Artikel).filter(
            ((Artikel.artart == 2) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.departement == 0)).all():

        for billjournal in db_session.query(Billjournal).filter(
                (func.lower(Billjournal.userinit) == (user_init).lower()) &  (Billjournal.artnr == artikel.artnr) &  (Billjournal.anzahl != 0) &  (Billjournal.departement == artikel.departement) &  (Billjournal.bill_datum == from_date) &  (Billjournal.betriebsnr == 0)).all():

            journal = db_session.query(Journal).filter(
                        (Journal._recid == billJournal._recid)).first()
            journal.betriebsnr = shift

            journal = db_session.query(Journal).first()

    return generate_output()