from functions.additional_functions import *
import decimal
from models import Artikel

def read_artikel1bl(case_type:int, artno:int, dept:int, aname:str, artart:int, betriebsno:int, actflag:bool):
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, artikel


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"t-artikel": t_artikel_list}

    def cr_artikel():

        nonlocal t_artikel_list, artikel


        nonlocal t_artikel
        nonlocal t_artikel_list


        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    if case_type == 1:

        if artno != 0:

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == artno) &  (Artikel.departement == dept)).first()

        elif aname != "":

            artikel = db_session.query(Artikel).filter(
                    (Artikel.bezeich == aname) &  (Artikel.departement == dept)).first()

        if artikel:
            cr_artikel()
    elif case_type == 2:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artno) &  (Artikel.departement == dept) &  (Artikel.artart == artart)).first()

        if artikel:
            cr_artikel()
    elif case_type == 3:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artno) &  (Artikel.departement == dept) &  (Artikel.activeFlag == actflag)).first()

        if not artikel:

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == artno) &  (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeFlag)).first()

        if artikel:
            cr_artikel()
    elif case_type == 4:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artno) &  (Artikel.departement == dept) &  (Artikel.betriebsnr == betriebsno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 5:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 8) |  (Artikel.artart == 9)) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()
    elif case_type == 6:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 5) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()
    elif case_type == 7:

        artikel = db_session.query(Artikel).filter(
                (Artikel.betriebsnr == betriebsno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 8:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 8) |  ((Artikel.artart == 9) &  (Artikel.artgrp != 0))) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()
    elif case_type == 9:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 8) |  ((Artikel.artart == 9) &  (Artikel.artgrp != 0))) &  (Artikel.activeflag == actflag) &  (Artikel.bezeich >= aname)).all():
            cr_artikel()
    elif case_type == 10:

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  ((Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.artnr == artno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 11:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.artnr == artno) &  (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 1) |  (Artikel.artart == 8) |  (Artikel.artart == 9))).all():
            cr_artikel()
    elif case_type == 12:

        if dept == None:
            dept = 0

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 2) |  (Artikel.artart == 5) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()
    elif case_type == 13:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()
    elif case_type == 14:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artart == 2) |  (Artikel.artart == 7)).first()

        if artikel:
            cr_artikel()
    elif case_type == 15:

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr == artno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 16:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  (Artikel.artart == artart) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()
    elif case_type == 17:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artno) &  (Artikel.departement == dept) &  (Artikel.artart == artart) &  (Artikel.pricetab == actflag)).first()

        if artikel:
            cr_artikel()
    elif case_type == 18:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  (Artikel.artart == artart) &  (Artikel.pricetab == actflag)).all():
            cr_artikel()
    elif case_type == 19:

        for t_artikel in query(t_artikel_list, filters=(lambda t_artikel :artikel.departement == dept and artikel.artart == artart and artikel.artnr >= artno and artikel.pricetab == actflag)):
            cr_artikel()
    elif case_type == 20:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  (Artikel.artnr == artno)).all():
            cr_artikel()
    elif case_type == 21:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artno) &  (Artikel.departement == dept) &  ((Artikel.artart == 4) |  (Artikel.artart == 6))).first()

        if artikel:
            cr_artikel()
    elif case_type == 22:

        if betriebsno == 7:

            artikel = db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (Artikel.artnr == artno) &  ((Artikel.artart == 4) |  (Artikel.artart == 7))).first()
        else:

            artikel = db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (Artikel.artnr == artno) &  ((Artikel.artart == 4) |  (Artikel.artart == 2) |  (Artikel.artart == 7))).first()

        if artikel:
            cr_artikel()
    elif case_type == 23:

        if betriebsno == 7:

            if artno == 1:

                for artikel in db_session.query(Artikel).filter(
                        (Artikel.departement == 0) &  ((Artikel.artart == 4) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():
                    cr_artikel()

            else:

                for artikel in db_session.query(Artikel).filter(
                        (Artikel.departement == 0) &  ((Artikel.artart == 4) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():
                    cr_artikel()

        else:

            if artno == 1:

                for artikel in db_session.query(Artikel).filter(
                        (Artikel.departement == 0) &  ((Artikel.artart == 4) |  (Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():
                    cr_artikel()

            else:

                for artikel in db_session.query(Artikel).filter(
                        (Artikel.departement == 0) &  ((Artikel.artart == 4) |  (Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():
                    cr_artikel()

    elif case_type == 24:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 8) |  (Artikel.artart == 9)) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 5) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()
    elif case_type == 25:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 8) |  ((Artikel.artart == 9) &  (Artikel.artgrp != 0))) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 5) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag == actflag)).all():
            cr_artikel()
    elif case_type == 26:

        artikel = db_session.query(Artikel).filter(
                (Artikel.bezeich == aname) &  (Artikel.departement == dept) &  (Artikel.artnr != artno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 27:

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  (Artikel.zwkum == artno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 28:

        artikel = db_session.query(Artikel).filter(
                (Artikel.endkum == artno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 29:

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == dept)).first()

        if artikel:
            cr_artikel()
    elif case_type == 30:

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 8)) &  (Artikel.artnr == artno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 31:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artart == 0) &  (Artikel.artgrp == artno)).first()

        if artikel:
            cr_artikel()
    elif case_type == 32:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.artart == artart) &  (Artikel.departement == dept)).all():
            cr_artikel()
    elif case_type == 33:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 8))).all():
            cr_artikel()
    elif case_type == 34:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artno) &  (Artikel.departement == dept) &  (Artikel.artart == artart) &  (Artikel.activeflag == actflag)).first()

        if artikel:
            cr_artikel()

    return generate_output()