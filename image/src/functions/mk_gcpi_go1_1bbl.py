from functions.additional_functions import *
import decimal
from datetime import date
from models import Gc_giro

def mk_gcpi_go1_1bbl(chequeno:str, duedate:date, postdate:date, pay_amount:decimal, docu_nr:str):
    gc_giro = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_giro


        return {}


    gc_giro = db_session.query(Gc_giro).filter(
            (Gc_giro.gironum == chequeno)).first()

    if gc_giro:
        gc_giro.giro_status = 1
        gc_giro.duedate = duedate
        gc_giro.postedDate = postdate
        gc_giro.betrag = pay_amount
        gc_giro.docu_nr = docu_nr

        gc_giro = db_session.query(Gc_giro).first()


    return generate_output()