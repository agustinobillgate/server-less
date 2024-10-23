from functions.additional_functions import *
import decimal
from datetime import date
from models import Uebertrag

def gl_outstandbl(date1:date, int1:int, deci1:decimal):
    uebertrag = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal uebertrag
        nonlocal date1, int1, deci1


        return {}


    uebertrag = db_session.query(Uebertrag).filter(
             (Uebertrag.datum == date1) & (Uebertrag.betriebsnr == int1)).first()

    if uebertrag:
        uebertrag.betrag =  to_decimal(deci1)


        pass

    return generate_output()