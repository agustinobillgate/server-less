from functions.additional_functions import *
import decimal
from datetime import date
from models import Uebertrag

def gl_outstandbl(date1:date, int1:int, deci1:decimal):
    uebertrag = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal uebertrag


        return {}


    uebertrag = db_session.query(Uebertrag).filter(
            (Uebertrag.datum == date1) &  (Uebertrag.betriebsnr == int1)).first()

    if uebertrag:
        uebertrag.betrag = deci1


    return generate_output()