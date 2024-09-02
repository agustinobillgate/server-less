from functions.additional_functions import *
import decimal
from models import Artikel, Argt_line, Arrangement

def nsargt_admin_btn_delbl(rec_id:int, q1_list_argtnr:int):
    err = 0
    art_dept = 0
    art_bez = ""
    artikel = argt_line = arrangement = None

    artikel1 = None

    Artikel1 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, art_dept, art_bez, artikel, argt_line, arrangement
        nonlocal artikel1


        nonlocal artikel1
        return {"err": err, "art_dept": art_dept, "art_bez": art_bez}


    artikel1 = db_session.query(Artikel1).filter(
            (Artikel1.artart == 0) &  (Artikel1.artgrp == q1_list_argtnr)).first()

    if artikel1:
        err = 1
        art_dept = artikel1.departement
        art_bez = artikel1.bezeich

        return generate_output()

    for argt_line in db_session.query(Argt_line).filter(
            (Argt_line.argtnr == q1_list_argtnr)).all():
        db_session.delete(argt_line)

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement._recid == rec_id)).first()

    arrangement = db_session.query(Arrangement).first()
    db_session.delete(arrangement)

    return generate_output()