#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Billjournal, Artikel

def close_shiftbl(user_init:string, from_date:date, shift:int):

    prepare_cache ([Billjournal, Artikel])

    billjournal = artikel = None

    journal = None

    Journal = create_buffer("Journal",Billjournal)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billjournal, artikel
        nonlocal user_init, from_date, shift
        nonlocal journal


        nonlocal journal

        return {}


    for artikel in db_session.query(Artikel).filter(
             ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.departement == 0)).order_by(Artikel._recid).all():

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.userinit == (user_init).lower()) & (Billjournal.artnr == artikel.artnr) & (Billjournal.anzahl != 0) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == from_date) & (Billjournal.betriebsnr == 0)).order_by(Billjournal._recid).all():

            journal = db_session.query(Journal).filter(Journal._recid == billjournal._recid).with_for_update().first()
            journal.betriebsnr = shift

    return generate_output()