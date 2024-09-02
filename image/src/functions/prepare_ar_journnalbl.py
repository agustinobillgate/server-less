from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Artikel, Hoteldpt

def prepare_ar_journnalbl():
    min_dept:int = 99
    max_dept:int = 0
    min_art:int = 9999
    max_art:int = 0
    from_date = None
    to_date = None
    from_art = 0
    to_art = 0
    from_dept = 0
    to_dept = 0
    depname1 = ""
    depname2 = ""
    htparam = artikel = hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal min_dept, max_dept, min_art, max_art, from_date, to_date, from_art, to_art, from_dept, to_dept, depname1, depname2, htparam, artikel, hoteldpt


        return {"from_date": from_date, "to_date": to_date, "from_art": from_art, "to_art": to_art, "from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = htparam.fdate
    to_date = htparam.fdate

    for artikel in db_session.query(Artikel).filter(
            (Artikel.activeflag) &  ((Artikel.artart == 2) |  (Artikel.artart == 7))).all():

        if min_art > artikel.artnr:
            min_art = artikel.artnr

        if max_art < artikel.artnr:
            max_art = artikel.artnr

    for hoteldpt in db_session.query(Hoteldpt).all():

        if min_dept > hoteldpt.num:
            min_dept = hoteldpt.num

        if max_dept < hoteldpt.num:
            max_dept = hoteldpt.num
    from_art = min_art
    to_art = max_art
    from_dept = min_dept
    to_dept = min_dept

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == from_dept)).first()
    depname1 = hoteldpt.depart

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == to_dept)).first()
    depname2 = hoteldpt.depart

    return generate_output()